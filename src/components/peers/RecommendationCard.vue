<template>
    <md-card md-with-hover
             class="recommendationsCard">
        <md-card-header class="fullWidth">
            <md-avatar>
                <md-avatar>
                    <img :src="data.image"
                         :alt="data.name">
                </md-avatar>
            </md-avatar>
            <div class="md-title">{{data.name}}</div>
            <div class="md-subhead">
                <topic-chip v-for="prof in data.proficiencies"
                            :key="prof"
                            linkTo="/view/peers">
                    {{prof}}
                </topic-chip>
            </div>
            <md-button class="type"> {{ data.recommendationType }}</md-button>
            <md-button class="date"> {{ meetingTime }}</md-button>
        </md-card-header>
        <md-card-content class="fullWidth flex">
            <md-input-container class="autoComplete">
                <label>Meeting Location</label>
                <md-autocomplete v-model="meetingLocation"
                                 :list="meetingHistory"
                                 :filter-list="findItem"></md-autocomplete>
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
import { Vue, Component, Prop } from "av-ts";
import UserService from "../../services/UserService";

import TopicChip from "../util/TopicChip.vue";

@Component({
    components: {
        TopicChip
    }
})
export default class RecommendationCard extends Vue {
    @Prop data;

    meetingLocation = "";

    findItem(possibleList) {
        return possibleList.filter(x => x.name.toLowerCase().indexOf(this.meetingLocation.toLowerCase()) >= 0);
    }

    get meetingTime() {
        const dayToEnglish = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
        const meetDate = this.data.availableTime as Date;

        const date = `${dayToEnglish[meetDate.getDay()]} ${meetDate.getDate()}/${meetDate.getMonth()}`;
        const time = `${meetDate.getHours()}:${meetDate.getMinutes()}`;
        return date + " " + time;
    }
    get meetingHistory() {
        return UserService.getMeetingHistory();
    }
}
</script>
