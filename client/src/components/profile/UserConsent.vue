<template>
    <md-layout md-flex="100" class="flexColumn">
        <h2>Consent form for {{ courseCode }}:</h2>
        <p v-if="response">Current Response: {{ response }}</p>
        <md-card>
            {{ pConsentForm.text }}
        </md-card>
        <span class="">
            <md-button class="md-raised md-primary"
                @click="alterConsent(true)">Accept</md-button>
            <md-button class="md-raised"
                @click="alterConsent(false)">Decline</md-button>
        </span>
    </md-layout>
</template>

<style scoped>

.componentSeparator{
    flex:auto !important;
}

.flexColumn {
    flex-direction: column;
}

.paddedTop {
    padding-top:20px;
}

.rightAlign {
    justify-content: flex-end;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";

import { CourseUser, ConsentForm } from "../../interfaces/models";
import UserService from "../../services/UserService";
import Fetcher from "../../services/Fetcher";
import { addEventsToQueue } from "../../util";


@Component({
    components:{
    }
})
export default class UserConsentView extends Vue {

    pCourseCode = "";

    pResponse: string | undefined = undefined;

    pCourseUser: CourseUser | undefined = undefined;

    pConsentForm: ConsentForm | undefined = undefined;

    get courseCode() {
        return this.pCourseCode;
    }

    set courseCode(newCode) {
        this.pCourseCode = newCode;
    }

    get response() {
        return this.pResponse;
    }

    set response(newResp) {
        this.pResponse = newResp;
    }

    hasResponded() {
        return this.pResponse && this.pResponse !== undefined;
    }

    updateCourseUser(user: CourseUser) {
        this.pCourseCode = user.course.courseCode;
        this.pCourseUser = user;
    }

    setConsentForm(consentForm: ConsentForm | undefined) {
        if (consentForm !== undefined && consentForm.text) {
            this.pConsentForm = consentForm;
        } else {
            this.pConsentForm = {
                text: "",
                author: this.pCourseUser!
            };
        }
    }

    alterConsent(newConsent: boolean) {
        UserService.sendConsent(newConsent).then(resp => this.updateUserConsent(resp));
    }

    updateUserConsent(newConsent: string) {
        this.response = newConsent;
        addEventsToQueue([{
            id: -6,
            name: "Consent Altered",
            description: "Response is now: " + newConsent,
            icon: "cached"
        }]);
        this.$router.push({ "name": "profile" });
    }


    @Lifecycle
    created() {
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateCourseUser);
        Fetcher.get(UserService.getConsentForm)
            .on(this.setConsentForm);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateCourseUser);
        Fetcher.get(UserService.getConsentForm)
            .off(this.setConsentForm);
    }
}
</script>
