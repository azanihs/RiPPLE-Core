<template>
    <md-layout>
        <md-card class="fullWidth">
            <md-layout md-flex="100">
                <md-card class="componentSeparator">
                    <timeline :eventLookup="eventLookup" :sortedDates="sortedDates"></timeline>
                </md-card>
            </md-layout>
            <md-layout md-flex="100">
                <md-card>
                    <h3>Current Connections</h3>
                    <current-connection-search :connections="connections">
                    </current-connection-search>
                </md-card>
            </md-layout>
        </md-card>
    </md-layout>
</template>

<style scoped>
.chartHeader {
    width: 100%;
    text-align: center;
    margin-top: 0px;
    color: #999;
}

.fullWidth {
    width: 100%;
    user-select: none;
    padding: 0px !important;
    overflow: hidden;
}

.overflowMobile {
    overflow: auto;
}

</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { IDate, IEvent, IEventLookup, ILocalisedEvent, ITime, IUser } from "../../interfaces/models";

import EventService from "../../services/EventService";
import UserService from "../../services/UserService";
import Fetcher from "../../services/Fetcher";

import CurrentConnectionSearch from "./CurrentConnectionSearch.vue";
import OverviewDescription from "../util/OverviewDescription.vue";
import Timeline from "../util/Timeline.vue";

@Component({
    components: {
        CurrentConnectionSearch,
        OverviewDescription,
        Timeline
    }
})
export default class Meetings extends Vue {

    pCurrentConnections: IUser[] = [];
    pEventLookup: IEventLookup = {};

    updateCurrentConnections(newConnections: IUser[]) {
        this.pCurrentConnections = newConnections;
    };

    updateEvents(newEvents: IEvent[]) {
        this.pEventLookup = this.createEventLookup(newEvents);
    };

    createEventLookup(events: IEvent[]): IEventLookup {
        const nowUTC = this.nowUTC();
        let eventLookup: IEventLookup = {};

        events.map((event: IEvent) => {
            const days = Math.abs(event.dayTime.day.id % 7 - nowUTC.day);
            const nowDate: Date = new Date();
            const eventDate: Date = this.localisedEventDate(nowDate, days, event.dayTime.time);
            const localisedEvent = this.localiseEvent(eventDate, event);
            this.addlocalisedEvent(eventLookup, localisedEvent);
        });

        return eventLookup;
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

    addDays(date: string, days: number): Date {
        // From: https://stackoverflow.com/questions/563406/add-days-to-javascript-date
        let result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    }

    localisedEventDate(now: Date, days: number, time: ITime): Date {
        let eventDate: Date = this.addDays(now.toUTCString(), days);
        eventDate.setHours(time.start.hour);
        eventDate.setMinutes(0);
        eventDate.setSeconds(0);
        eventDate.setMilliseconds(0);
        return eventDate;
    }

    localiseEvent(date: Date, event: IEvent) {
        const localisedEventDate: ILocalisedEvent = {
            date: date.toString(),
            user: event.user,
            topics: event.topics,
            location: event.location
        };
        return localisedEventDate;
    }

    addlocalisedEvent( eventLookup: IEventLookup, localisedEvent: ILocalisedEvent) {
        let date = new Date(localisedEvent.date).toDateString();
        if (eventLookup) {
            if (eventLookup[date] === undefined) {
                eventLookup[date] = [localisedEvent];
            } else {
                eventLookup[date].push(localisedEvent);
            }
            return eventLookup;
        } else {
            let newLookup: IEventLookup = {};
            newLookup[date] = [localisedEvent];
            return newLookup;
        }
    }


    @Lifecycle
    created() {
        UserService.getRecommendedConnections({ count: 3 }).then(this.updateCurrentConnections);
        Fetcher.get(EventService.getWeekEvents).on(this.updateEvents);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(EventService.getWeekEvents).off(this.updateEvents);
    }

    get connections() {
        return this.pCurrentConnections;
    }

    get eventLookup() {
        return this.pEventLookup;
    }

    get sortedDates() {
        let dates: string[] = Object.keys(this.pEventLookup);
        let sortedDates: Date[] = [];
        if (dates.length > 0) {
            dates.map(date => sortedDates.push(new Date(date)));
            sortedDates.sort((a, b) => a.getTime() - b.getTime());
        }

        return sortedDates;
    }
}
</script>
