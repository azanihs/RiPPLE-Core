<template>
    <md-layout class="buttonContainer">
        <md-button @click="back">
            Return to Questions
        </md-button>
        <md-button @click="randomQuestion">
            Go To Random Question
        </md-button>
        <md-button @click="recommendations">
            Go to Recommendations
        </md-button>
    </md-layout>
</template>

<style scoped>
    .buttonContainer {
        width: 100%;
        justify-content: space-between;
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
