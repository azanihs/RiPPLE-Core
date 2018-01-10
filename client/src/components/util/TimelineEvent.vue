<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100"
                   class="componentSeparator">
            <md-card md-with-hover
                     class="recommendationsCard">
                <md-card-header class="fullWidth">
                    <md-avatar>
                        <md-avatar>
                            <img :src="user.image"
                                 :alt="user.name">
                        </md-avatar>
                    </md-avatar>
                    <div class="md-title">{{user.name}}</div>
                    <div class="md-subhead">
                        <topic-chip v-for="prof in user.proficiencies"
                                    :key="prof"
                                    linkTo="/view/peers">
                            {{prof}}
                        </topic-chip>
                    </div>
                    <md-button class="type"> {{ user.recommendationType }}</md-button>
                    <md-button class="date"> {{ meetingTime }}</md-button>
                </md-card-header>
                <md-card-content class="fullWidth flex">
                    <label>Meeting Location</label>
                    <label>{{ location }}</label>
                </md-card-content>

                <md-card-actions>
                    <md-button>Ignore</md-button>
                    <md-button>
                        <slot></slot>
                    </md-button>
                </md-card-actions>
            </md-card>
        </md-layout>
    </md-layout>
</template>

<style scoped>
.md-subhead {
    opacity: 1 !important;
}

.fullWidth {
    width: 100%;
}

.flex {
    display: flex;
    flex: 1;
    min-width: 100%;
    padding-bottom: 0px;
}

.type {
    position: absolute;
    top: 8px;
    right: 8px;
    font-size: 10px;
}

.date {
    position: absolute;
    bottom: 8px;
    right: 8px;
    font-size: 10px;
}

.autoComplete {
    margin-bottom: 0px;
}
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { ILocalisedEvent } from "../../interfaces/models";

import TopicChip from "../util/TopicChip.vue";

@Component({
    components: {
        TopicChip
    }
})
export default class TimelineEvent extends Vue {
    @Prop event = p<ILocalisedEvent>({
        required: true
    });

    formatAMPM(date: Date): string {
        // From: https://stackoverflow.com/questions/8888491/how-do-you-display-javascript-datetime-in-12-hour-am-pm-format
        let hours = date.getHours();
        let minutes = date.getMinutes();
        const ampm = hours >= 12 ? "pm" : "am";
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        const displayMins = minutes < 10 ? "0" + minutes : minutes.toString();
        const strTime = hours + ":" + displayMins + " " + ampm;
        return strTime;
    }

    get time() {
        if (this.event) {
            return this.formatAMPM(new Date(this.event.date));
        } else {
            return "";
        }
    }

    get user() {
        return this.event ? this.event.user : "";
    }

    get location() {
        return this.event ? this.event.location : "";
    }
}
</script>
