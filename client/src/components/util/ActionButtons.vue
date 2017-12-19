<template>
    <md-layout md-flex="100" class="buttonContainer">
        <md-layout>
            <md-button
                @click="back()">
                <md-icon>keyboard_return</md-icon>
                <span>Return</span>
            </md-button>
            <slot name="centreLeft"></slot>
        </md-layout>
        <md-layout class="right">
            <slot name="centreRight"></slot>
            <slot name="right"></slot>
        </md-layout>

        <div class="border">
            <hr />
        </div>
    </md-layout>
</template>

<style scoped>
.border {
    width: 100%;
    padding: 0px;
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
    margin-bottom: 0.5em;
}

.right {
    justify-content:flex-end
}
</style>

<script lang="ts">
import { Vue, Component } from "av-ts";

@Component()
export default class ActionButtons extends Vue {

    back() {
        this.$router.go(-1);
    }
}
</script>
