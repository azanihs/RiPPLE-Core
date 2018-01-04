<template>
    <md-layout md-flex="100">
        <timeline-day></timeline-day>
    </md-layout>
</template>

<style scoped>
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import { IDate, IEvent } from "../../interfaces/models";

import TimelineDay from "./TimelineDay.vue";

@Component({
    components: {
        TimelineDay
    }
})
export default class Timeline extends Vue {
    @Prop
    events = p<IEvent[]>({
        required: true
    });

    pNowUTC: IDate;
    // id = day difference between today and event day
    pEventLookup: {[id: number]: IEvent[]} = {};

    createEventLookup() {
        // Create the UTC Date
        this.pNowUTC = this.nowUTC();

        this.events.map((event: IEvent) => {
            const days = Math.abs(event.dayTime.day.id % 7 - this.pNowUTC.day);
            return days;
        });
    }

    nowUTC(): IDate {
        const now = new Date();

        const year = now.getUTCFullYear();
        const month = now.getUTCMonth();
        const date = now.getUTCDate();
        const day = now.getUTCDay();
        const hour = now.getUTCHours();
        const minute = now.getUTCMinutes();
        const second = 0;
        const millisecond = 0;

        const utcDate = {
            year,
            month,
            date,
            day,
            hour,
            minute,
            second,
            millisecond
        };

        return utcDate;
    };

    @Lifecycle
    created() {
        this.createEventLookup();
    }
}
</script>
