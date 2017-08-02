<template>
    <router-link v-if="linkTo" :to="linkTo" class="topicChipLink">
        <md-chip class="topicChip">
            <slot></slot>
        </md-chip>
    </router-link>
    <div v-else>
        <md-chip class="topicChip">
            <slot></slot>
        </md-chip>
    </div>
</template>

<style scoped>
a.topicChipLink,
a.topicChipLink:visited {
    color: #333;
    text-decoration: none;
    transition: 500ms ease background-color, 500ms ease color;
}

a.topicChipLink:hover {
    color: #eee;
    text-decoration: none;
}

.md-chip.topicChip {
    margin-right: 5px;
    background-color: #fff;
    border: 1px solid #ccc;
    transition: 500ms ease background-color;
}

.md-chip.topicChip:hover {
    background-color: #333;
    color: #eee;
}
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";

@Component()
export default class TopicChip extends Vue {
    @Prop linkTo = p({
        type: String
    });
}
</script>
