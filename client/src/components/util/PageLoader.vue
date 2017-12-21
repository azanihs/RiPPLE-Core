<template>
    <transition name="fade">
        <div class="loader" v-if="condition"
            :class = "{'mobileStyle': mobileMode}">
            <md-spinner class="progressSpinner" :md-size="300" :md-stroke="1" md-indeterminate></md-spinner>
            <span class="loaderContent">Loading Content</span>
        </div>
    </transition>
</template>

<style scoped>
    .fade-enter-active, .fade-leave-active {
        transition: opacity 250ms ease;
    }

    .fade-enter, .fade-leave-to {
        opacity: 0
    }

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

        background-color: #f2f2f2;
        transform: translate3d(0px, 0px, 0px);
        z-index: 10000;
    }

    .mobileStyle {
        left: 0px !important;
        width: 100% !important;
    }

    .loaderContent {
        position: absolute;
        color: #333;
    }
</style>

<script lang="ts">
    import { Vue, Component, Prop, p, Lifecycle } from "av-ts";
    import ApplicationService from "../../services/ApplicationService";

    @Component
    export default class PageLoader extends Vue {
        @Prop condition = p<boolean>({
            required: true
        });

        mobileMode: boolean = false;

        @Lifecycle
        created() {
            this.mobileMode = ApplicationService.getMobileMode();
        }

    }
</script>
