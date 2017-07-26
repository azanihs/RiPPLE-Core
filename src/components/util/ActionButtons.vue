<template>
    <md-layout class="buttonContainer">
        <md-button @click="back">
            <md-icon>keyboard_return</md-icon> Return
            <md-tooltip>Return To Questions</md-tooltip>
        </md-button>
        <md-button @click="randomQuestion">
            Random Question
            <md-icon>shuffle</md-icon>
            <md-tooltip>Random Question</md-tooltip>
        </md-button>
    </md-layout>
</template>

<style scoped>
.buttonContainer {
    width: 100%;
    justify-content: space-between;
    margin-bottom: 2em;
    border-bottom: 1px solid #ddd;
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
