<template>
    <md-layout md-flex="100">
        <timeline-day></timeline-day>
    </md-layout>
</template>

<style scoped>
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { IEventLookup } from "../../interfaces/models";

import TimelineDay from "./TimelineDay.vue";

@Component({
    components: {
        TimelineDay
    }
})
export default class Timeline extends Vue {
    @Prop eventLookup = p<IEventLookup>({
        required: true
    });
}
</script>
