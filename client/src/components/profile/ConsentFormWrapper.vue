<template>
    <md-layout md-flex="100" md-gutter>
        <consent-form class="hoistAboveOverlay" v-if="consentForm" @change="updateUserConsent" :consentForm="consentForm" :courseCode="courseCode" :response="response"></consent-form>
        <md-layout md-class="hoistAboveOverlay" flex="100" md-gutter v-else>
            <md-card>
                Your course instructor has not set up a consent form for your course.
                You will be unable to use this tool until the consent form is set up.
            </md-card>
        </md-layout>
        <div v-if="response === undefined" class="overlay"></div>
    </md-layout>
</template>

<style scoped>
.hoistAboveOverlay {
    z-index: 2;
    margin-top: 8px;
}
.overlay {
    position: fixed;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;
    z-index: 1;
    background-color: #333;
    opacity: 0.25;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { IConsentForm, ICourseUser } from "../../interfaces/models";

import { addEventsToQueue } from "../../util";

import ConsentForm from "./ConsentForm.vue";

import UserService from "../../services/UserService";
import Fetcher from "../../services/Fetcher";

@Component({
    components: {
        ConsentForm
    }
})
export default class ConsentFormWrapper extends Vue {
    pCourseUser: ICourseUser | undefined = undefined;
    pCourseCode: string | undefined = undefined;
    pResponse: boolean | undefined = undefined;
    pConsentForm: IConsentForm | undefined = undefined;

    updateUserConsent(newConsent: boolean) {
        this.updateConsentResponse(newConsent);
        UserService.sendConsent(newConsent);

        addEventsToQueue([{
            name: "Consent Altered",
            description: "Response is now: " + (newConsent == true ? "Accepted" : "Declined"),
            icon: "cached"
        }]);

        this.$router.push({ "name": "overview" });
    }

    updateCourseUser(user: ICourseUser) {
        this.pCourseCode = user.course.courseCode;
        this.pCourseUser = user;
    }

    setConsentForm(consentForm: IConsentForm | undefined) {
        if (consentForm !== undefined && consentForm.content) {
            this.pConsentForm = consentForm;
        } else {
            this.pConsentForm = undefined;
        }
    }

    updateConsentResponse(newResponse: boolean | undefined) {
        this.pResponse = newResponse;
    }

    @Lifecycle
    created() {
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateCourseUser);
        Fetcher.get(UserService.getConsentForm)
            .on(this.setConsentForm);

        // Don't subscribe to this queue; since we are the ones managing it
        UserService.getUserConsentFormResponse()
            .then(x => this.updateConsentResponse(x));
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateCourseUser);
        Fetcher.get(UserService.getConsentForm)
            .off(this.setConsentForm);
    }

    get courseCode() {
        return this.pCourseCode;
    }
    get consentForm() {
        return this.pConsentForm;
    }
    get response() {
        return this.pResponse;
    }
}
</script>
