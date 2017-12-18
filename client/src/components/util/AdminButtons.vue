<template>
    <md-layout class="buttonContainer">
        <action-buttons>
            <md-button
                class="primary-colour"
                slot="centreRight"
                @click="saveQuestion">
                <span>Save Question</span>
            </md-button>
            <md-button
                class="md-warn"
                slot="right"
                @click="deleteQuestion">
                <span>Delete Question</span>
            </md-button>
        </action-buttons>
    </md-layout>
</template>

<style scoped>
.primary-colour {
    color:#256
}
.buttonContainer {
    width: 100%;
    justify-content: space-between;
    margin-bottom: 0.5;
}
</style>

<script lang="ts">
import { Vue, Component } from "av-ts";
import ActionButtons from "./ActionButtons.vue";

@Component({
    components: {
        ActionButtons
    }
})

export default class AdminButtons extends Vue {
    saveQuestion() {
        this.$emit("saveQuestion");
    }

    deleteQuestion() {
        this.$emit("deleteQuestion");
    }
}
</script>
