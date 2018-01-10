<template>
    <md-layout md-flex="100"
               class="componentSeparator">
        <md-card md-with-hover>
            <md-layout md-flex="10">
                <h3>{{ time }}</h3>
            </md-layout>
            <md-layout md-flex="25">
                <md-avatar>
                    <md-avatar>
                        <img :src="user.image"
                             :alt="user.name">
                    </md-avatar>
                </md-avatar>
                <md-layout md-flex="100" class="centerContainer">
                    <div class="center">{{ user.name }}</div>
                </md-layout>
            </md-layout>
            <md-layout md-flex="25">
                <div class="md-subhead">
                    <topic-chip v-for="prof in user.proficiencies"
                                :key="prof"
                                linkTo="/view/peers">
                        {{prof}}
                    </topic-chip>
                </div>
            </md-layout>
            <md-layout md-flex="20">
                <md-layout md-flex="100">
                    <label>Meeting Location</label>
                </md-layout>
                <md-layout md-flex="100">
                    <label>{{ location }}</label>
                </md-layout>
            </md-layout>
            <md-layout md-flex="20" class="centerContainer">
                <md-button class="center">Cancel</md-button>
            </md-layout>
        </md-card>
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

.centerContainer {
    position: relative;
}

.center {
    position:absolute;
    left:50%;
    transform: translateX(-50%);
    -webkit-transform: translateX(-50%);
}

.eventUserName {
    text-align: center;
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
