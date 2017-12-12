<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100">
            <h2>Consent form for {{ courseCode }}:</h2>
        </md-layout>

        <md-card class="card">
            <span v-html="consentForm.content"></span>
            <p v-if="response">Current Response: {{ response }}</p>
            <md-layout md-flex="100" class="buttonContainer" md-gutter>
                <md-button class="md-raised md-primary"
                    @click="alterConsent(true)">I Accept</md-button>
                <md-button class="md-raised"
                    @click="alterConsent(false)">I Decline</md-button>
            </md-layout>
        </md-card>
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
import UserService from "../../services/UserService";

@Component()
export default class ConsentForm extends Vue {

    @Prop consentForm = p<IConsentForm>({
        required: true
    });

    @Prop courseCode = p<string>({
        required: true
    });

    @Prop response = p<string | undefined>({
        required: false
    });

    hasResponded() {
        return this.response && this.response !== undefined;
    }

    alterConsent(newConsent: boolean) {
        UserService.sendConsent(newConsent)
            .then(newResponse => this.updateUserConsent(newResponse));
    }

    updateUserConsent(newConsent: string) {
        this.$emit("change", newConsent);
    }
}
</script>
