<template>
    <md-layout class="buttonContainer">
        <md-button @click="back">
            Return to Questions
        </md-button>
        <md-button @click="randomQuestion">
            Go To Random Question
        </md-button>
        <md-button @click="recommendations"
                   class="md-icon-button md-warn">
            <md-icon>error_outline</md-icon>
            <md-tooltip>Report Question</md-tooltip>
        </md-button>
    </md-layout>
</template>

<style scoped>
    .buttonContainer {
        width: 100%;
        justify-content: space-between;
        margin-bottom: 2em;
    }
</style>

<script lang="ts">
    import { Vue, Component } from "av-ts";

    @Component()
    export default class ActionButtons extends Vue {

        back() {
            this.$emit("back");
        }
        randomQuestion() {
            this.$emit("randomQuestion");
        }
        recommendations() {
            this.$emit("recommendations");
        }

    }
</script>
