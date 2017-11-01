<template>
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
            <md-input-container class="autoComplete">
                <label>Meeting Location</label>
                <md-autocomplete v-model="meetingLocation"
                                 :filterList="findItem"
                                 :list="meetingHistory"></md-autocomplete>
            </md-input-container>

        </md-card-content>

        <md-card-actions>
            <md-button>Ignore</md-button>
            <md-button>
                <slot></slot>
            </md-button>
        </md-card-actions>
    </md-card>
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
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import { User } from "../../interfaces/models";

import UserService from "../../services/UserService";
import Fetcher from "../../services/Fetcher";

import TopicChip from "../util/TopicChip.vue";

@Component({
    components: {
        TopicChip
    }
})
export default class RecommendationCard extends Vue {
    @Prop user = p({
        required: true
    }) as User;

    pMeetingHistory = [];
    updateMeetingHistory(newHistory) {
        this.pMeetingHistory = newHistory;
    }

    meetingLocation = "";

    @Lifecycle
    created() {
        Fetcher.get(UserService.getMeetingHistory)
            .on(this.updateMeetingHistory);
    }

    findItem(list, possibleList) {
        return possibleList.filter(x => x.toLowerCase().indexOf(this.meetingLocation.toLowerCase()) >= 0);
    }

    get meetingTime() {
        const dayToEnglish = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
        const meetDate = this.user.availableTime as Date;

        const date = `${dayToEnglish[meetDate.getDay()]} ${meetDate.getDate()}/${meetDate.getMonth()}`;
        const time = `${meetDate.getHours()}:${meetDate.getMinutes()}`;
        return date + " " + time;
    }

    get meetingHistory() {
        return this.pMeetingHistory;
    }
}
</script>
