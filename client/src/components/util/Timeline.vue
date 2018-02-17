<template>
    <md-layout md-flex="100">
        <timeline-day v-for="date in sortedDates"
            :key="date.toDateString()"
            :date="date"
            :events="eventLookup[date.toDateString()]"
            @change="change"
        ></timeline-day>
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

    @Prop sortedDates = p<Date[]>({
        required: true
    });

    change(id: number) {
        this.$emit("change", id);
    }
}
</script>
