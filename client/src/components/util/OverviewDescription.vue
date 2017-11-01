<template>
    <div class="descriptionContainer">
        <slot></slot>
    </div>
</template>

<style scoped>
.descriptionContainer {
    width: 100%;
    margin-bottom: 2em;
}

.descriptionContainer h2 {
    padding-top: 0.75em;
    padding-bottom: 0px;
}
</style>

<script lang="ts">
import { Vue, Component, Prop } from "av-ts";

@Component()
export default class OverviewDescription extends Vue { }
</script>
