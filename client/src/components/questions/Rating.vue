<template>
    <div class="iconContainer"
         :class="{disabled: disabled}">
        <md-tooltip v-if="disabled">
            You must attempt the question before you can rate it
        </md-tooltip>
        <md-button v-for="i in +max"
                   :disabled="disabled"
                   :key="i"
                   class="md-icon-button"
                   @click.native="changeRating"
                   @mouseover.native="previewRating"
                   @mouseout.native="mouseOut"
                   ref="icons">
            <md-icon class="halfSize"
                     v-bind:class="{'md-primary': (i-1) <= previewIndex}">{{icon}}</md-icon>
        </md-button>
    </div>
</template>
<style scoped>
.md-icon-button {
    margin: 0px !important;
}

.iconContainer {
    width: 100%;
    display: flex;
    flex-direction: inherit;
}

.md-icon {
    transition: 500ms color ease;
}

.md-icon:not(.md-primary) {
    color: #ccc !important;
}

.md-primary {
    color: #256 !important;
}

.iconContainer.disabled {
    cursor: not-allowed
}
</style>
<script lang="ts">
import { Vue, Component, Prop, Lifecycle, p } from "av-ts";
@Component()
export default class Rating extends Vue {
    // Max number of starts
    @Prop max;
    @Prop disabled = p({
        type: Boolean,
        default: false
    });

    @Prop icon = p({
        type: String,
        default: "star"
    }) as string;

    @Prop defaultIndex = p({
        type: Number,
        default: -1
    }) as number;

    // Current start selection
    selectedIndex = -1;
    previewIndex = -1;

    @Lifecycle
    created() {
        this.selectedIndex = this.defaultIndex;
        this.previewIndex = this.defaultIndex;
    }


    changeRating(e: MouseEvent) {
        if (this.disabled) return;

        // Check if the user clicked on child. If so, select the parent button
        let target = e.target as HTMLElement;
        if (target.tagName == "I") {
            target = target.parentElement;
        }
        const icons = this.$refs["icons"] as Array<Vue>;
        this.selectedIndex = icons.findIndex((x: Vue) => x.$el == target);
        this.$emit("input", this.selectedIndex);
    }

    previewRating(e: MouseEvent) {
        if (this.disabled) return;

        // Check if the user clicked on child. If so, select the parent button
        let target = e.target as HTMLElement;
        if (target.tagName == "I") {
            target = target.parentElement;
        }
        const icons = this.$refs["icons"] as Array<Vue>;
        this.previewIndex = icons.findIndex((x: Vue) => x.$el == target);
    }

    mouseOut(e: MouseEvent) {
        if (this.disabled) return;

        this.previewIndex = this.selectedIndex;
    }
}
</script>
