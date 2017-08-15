<template>
    <md-layout class="buttonContainer">
        <md-button @click="back">
            <md-icon>keyboard_return</md-icon>
            <span>Return</span>
            <md-tooltip>Return To Questions</md-tooltip>
        </md-button>
        <md-button class="md-warn"
                   @click="report">
            <span>Report Question</span>
            <md-icon>error_outline</md-icon>
        </md-button>
    
        <div class="border">
            <hr />
        </div>
    </md-layout>
</template>

<style scoped>
.border {
    width: 100%;
    padding: 0px 16px;
}

hr {
    width: 100%;
    display: block;
    text-align: center;
    border: none;
    border-bottom: 1px solid #ddd;
}

.buttonContainer {
    width: 100%;
    justify-content: space-between;
    margin-bottom: 1em;
    margin-left: -16px;
    margin-right: -16px;
}
</style>

<script lang="ts">
import { Vue, Component } from "av-ts";

@Component()
export default class ActionButtons extends Vue {

    back() {
        this.$emit("back");
    }
    report() {
        this.$emit("report");
    }

}
</script>
