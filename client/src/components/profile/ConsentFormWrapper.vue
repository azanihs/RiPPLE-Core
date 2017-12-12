<template>
    <consent-form v-if="consentForm" @change="updateUserConsent" :consentForm="consentForm" :courseCode="courseCode" :response="response"></consent-form>
    <md-layout md-flex="100" md-gutter v-else>
        <md-card>
            Your course instructor has not set up a consent form for your course.
            You will be unable to use this tool until the consent form is set up.
        </md-card>
    </md-layout>
</template>

<style scoped>

</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { IConsentForm, CourseUser } from "../../interfaces/models";

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
    pCourseUser: CourseUser | undefined = undefined;
    pCourseCode: string | undefined = undefined;
    pResponse: string | undefined = undefined;
    pConsentForm: IConsentForm | undefined = undefined;

    updateUserConsent(newConsent: string) {
        this.updateConsentResponse(newConsent);

        addEventsToQueue([{
            id: -6,
            name: "Consent Altered",
            description: "Response is now: " + newConsent,
            icon: "cached"
        }]);
        this.$router.push({ "name": "profile" });
    }

    updateCourseUser(user: CourseUser) {
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

    updateConsentResponse(newResponse: string) {
        this.pResponse = newResponse;
    }

    @Lifecycle
    created() {
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateCourseUser);
        Fetcher.get(UserService.getConsentForm)
            .on(this.setConsentForm);
        Fetcher.get(UserService.getUserConsentFormResponse)
            .on(this.updateConsentResponse);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateCourseUser);
        Fetcher.get(UserService.getConsentForm)
            .off(this.setConsentForm);
        Fetcher.get(UserService.getUserConsentFormResponse)
            .off(this.updateConsentResponse);
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
