<template>
    <div class="loader">
        <md-spinner class="progressSpinner" :md-size="300" :md-stroke="1" md-indeterminate></md-spinner>
        <span class="loaderContent">Loading Question</span>
    </div>
</template>

<style scoped>
    .loader {
        left: 16.25%;
        top: 0px;
        position: fixed;
        height: 100%;
        width: 83.75%;
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;

        opacity: 0.85;
        background-color: #f2f2f2;
        transform: translate3d(0px, 0px, 0px);
        z-index: 10000;
    }

    .loaderContent {
        position: absolute;
        color: #333;
    }
</style>

<script lang="ts">
    import { Vue, Component } from "av-ts";

    @Component
    export default class PageLoader extends Vue {}
</script>
