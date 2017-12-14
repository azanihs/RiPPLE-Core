<template>
    <md-layout md-flex="100" md-gutter>
        <md-layout md-flex="100" class="consentForm" md-gutter>
            <md-card class="card">
                <h2>Consent form for {{ courseCode }}:</h2>
                <md-layout md-flex="100">
                    <div v-html="consentForm.content"></div>
                </md-layout>
                <p>Current Response: {{ currentResponse }}</p>
                <md-layout md-flex="100" class="buttonContainer" md-gutter>
                    <md-button class="md-raised md-primary"
                        @click="alterConsent(true)">I Accept</md-button>
                    <md-button class="md-raised"
                        @click="alterConsent(false)">I Decline</md-button>
                </md-layout>
            </md-card>
        </md-layout>
    </md-layout>
</template>

<style scoped>
.card {
    margin-bottom: 1em;
}
.buttonContainer {
    border-top: 1px solid #ccc;

}
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";

import { IConsentForm } from "../../interfaces/models";

@Component()
export default class ConsentForm extends Vue {

    @Prop consentForm = p<IConsentForm>({
        required: true
    });

    @Prop courseCode = p<string>({
        required: true
    });

    @Prop response = p<boolean | undefined>({
        required: false
    });


    get currentResponse() {
        if (this.response === true) {
            return "Accepted";
        } else if (this.response === false) {
            return "Declined";
        }

        return "Unanswered";
    }

    hasResponded() {
        return this.response && this.response !== undefined;
    }

    alterConsent(newConsent: boolean) {
        this.$emit("change", newConsent);
    }
}
</script>
