<template>
        <router-link v-if="linkTo" :to="linkTo" class="topicChipLink" :class="[status]">
            <md-chip class="topicChip">
                <slot></slot>
            </md-chip>
        </router-link>
        <md-chip v-else class="topicChip" :class="[status]">
            <slot></slot>
        </md-chip>
</template>

<style>
.topicChip > .md-chip-container {
    max-width: 100px;
    overflow: hidden;
    white-space: pre;
    text-overflow: ellipsis;
}
</style>

<style scoped>

a.topicChipLink,
a.topicChipLink:visited {
    color: #333;
    text-decoration: none;
    transition: 500ms ease background-color, 500ms ease color;
}

a.topicChipLink:hover {
    color: #eee !important;
    text-decoration: none;
}

.md-chip.topicChip {
    background-color: #fff;

    margin-bottom: 5px;
    margin-right: 5px;
    border: 1px solid #ccc;
    transition: 500ms ease background-color;
    cursor: pointer;
}

.selected.md-chip.topicChip {
    background-color: #256;
    color: #f2f2f2;
}

.selected.md-chip.topicChip:hover {
    background-color: #fff;
    color: #222;
}

.disabled.md-chip.topicChip {
    color: #333;
}

</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import ResponsiveWrapper from "../util/ResponsiveWrapper.vue";

@Component({
    components: {
        ResponsiveWrapper
    }
})
export default class TopicChip extends Vue {
    @Prop linkTo = p<string>({
        required: false,
        default: ""
    });

    @Prop disabled = p<boolean>({
        required: false,
        default: false
    });

    get status() {
        return {
            disabled: this.disabled,
            selected: !this.disabled
        };
    }

}
</script>
