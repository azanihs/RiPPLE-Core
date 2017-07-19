<template>
    <div class="iconContainer">
        <md-button v-for="i in +max"
                   :key="i"
                   class="md-icon-button"
                   @click.native="changeRating"
                   ref="icons">
            <md-icon class="halfSize"
                     v-bind:class="{'md-primary': (i-1) <= selectedIndex}">{{icon}}</md-icon>
        </md-button>
    </div>
</template>
<style scoped>
    .iconContainer {
        width: 100%;
        display: flex;
        justify-content: space-between;
    }
    
    .md-icon:not(.md-primary) {
        color: #ccc !important;
    }
    
    .md-primary {
        color: #256 !important;
    }
    
    .md-button.md-icon-button {
        width: 27.5px;
        min-width: 27.5px;
        height: 27.5px;
        min-height: 27.5px;
    
        margin: 0 6px;
        padding: 8px;
        border-radius: 50%;
        line-height: 20px;
    }
    
    .halfSize {
        width: 20px;
        min-width: 20px;
        font-size: 20px;
        height: 20px;
        min-height: 20px;
    }
</style>
<script lang="ts">
    import { Vue, Component, Prop, Lifecycle, p } from "av-ts";
    @Component()
    export default class Rating extends Vue {
        // Max number of starts
        @Prop max;
        @Prop icon = p({
            type: String,
            default: "star"
        }) as string;

        @Prop defaultIndex = p({
            type: Number,
            default: -1
        }) as number;

        @Lifecycle
        created() {
            this.selectedIndex = this.defaultIndex;
        }

        // Current start selection
        selectedIndex = -1;
        changeRating(e: Event) {
            // Check if the user clicked on child. If so, select the parent button
            let target = e.target as HTMLElement;
            if (target.tagName == "I") {
                target = target.parentElement;
            }
            const icons = this.$refs["icons"] as Array<Vue>;
            this.selectedIndex = icons.findIndex((x: Vue) => x.$el == target);
            this.$emit("input", this.selectedIndex);
        }
    }
</script>
