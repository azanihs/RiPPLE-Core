<template>
    <md-layout>
        <md-layout md-hide-medium-and-up class="hidden" ref="onlyVisibleOnMobile"></md-layout>
        <span v-if="mobileMode"
                :class="classWhenMobile">
            <slot></slot>
        </span>
        <span v-else>
            <slot></slot>
        </span>
    </md-layout>
</template>

<style scoped>
    .hidden {
        width: 0px;
        height: 0px;
        flex-grow: 0;
        flex-basis: 0%;
    }

</style>


<script lang="ts">
import { Vue, Component, Prop, p, Lifecycle } from "av-ts";

@Component
export default class ResponsiveWrapper extends Vue {
    @Prop classWhenMobile = p<string>({
        required: false,
        default: "mobileStyle"
    });

    mobileMode = false;

    @Lifecycle
    mounted() {
        const visible = (this.$refs.onlyVisibleOnMobile as Vue);
        const isVisible = visible.$el;
        if (window.getComputedStyle(isVisible).display !== "none") {
            this.mobileMode = true;
        } else {
            this.mobileMode = false;
        }
        console.log(this.mobileMode);
    }
}

</script>
