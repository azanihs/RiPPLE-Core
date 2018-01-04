<template>
    <div>
        <h3>Wednesday, January 3</h3>
        <timeline-event v-for="event in events" :key="event" user="user"></timeline-event>
    </div>
</template>

<style scoped>
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { IEvent } from "../../interfaces/models";

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
    events = p<IEvent[]>({
        required: true
    });
}
</script>
