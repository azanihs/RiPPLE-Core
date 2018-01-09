<template>
    <md-layout md-flex="100">
        <h3>{{day}}</h3>
        <timeline-event v-for="(event, i) in events" :key="i" :event="event"></timeline-event>
    </md-layout>
</template>

<style scoped>
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { ILocalisedEvent } from "../../interfaces/models";

import TimelineEvent from "./TimelineEvent.vue";

@Component({
    components: {
        TimelineEvent
    }
})

export default class TimelineDay extends Vue {
    @Prop
    date = p<Date>({
        required: true
    });

    @Prop
    events = p<ILocalisedEvent[]>({
        required: true
    });

    pDays: string[] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday"];

    pMonths: string[] = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];

    get day() {
        if (this.date) {
            const weekDay: string = this.pDays[this.date.getDay()];
            const header: string = `${weekDay}, ${this.pMonths[this.date.getMonth()]} ${this.date.getDate()}`;
            return header;
        } else {
            return "";
        }
    }
}
</script>
