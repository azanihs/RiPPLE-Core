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
            <label>Meeting Location:</br>{{ location }}</label>
        </md-card-content>

        <md-card-actions>
            <md-button @click="ignoreRecommendation">Ignore</md-button>
            <md-button @click="acceptRecommendation">Accept</md-button>
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
import { IUser, IRecommendation } from "../../interfaces/models";
import UserService from "../../services/UserService";
import Fetcher from "../../services/Fetcher";
import TopicChip from "../util/TopicChip.vue";
import { serverToLocal } from "../../util";

interface IMeetingHistory {
    name: string,
    id: number
};

@Component({
    components: {
        TopicChip
    }
})
export default class RecommendationReviewCard extends Vue {
    @Prop recommendation = p<IRecommendation>({
        required: true
    });

    pMeetingHistory: IMeetingHistory[] = [];
    updateMeetingHistory(newHistory: IMeetingHistory[]) {
        this.pMeetingHistory = newHistory;
    }

    meetingLocation = "";

    @Lifecycle
    created() {
        Fetcher.get(UserService.getMeetingHistory)
            .on(this.updateMeetingHistory);
    }

    findItem(toSearch: IMeetingHistory[], query: string) {
        return toSearch.filter(x => x.name.toLowerCase().indexOf(query.toLowerCase()) >= 0);
    }

    ignoreRecommendation() {
        this.$emit("change", this.recommendation.id, "rejected");
    }

    acceptRecommendation() {
        this.$emit("change", this.recommendation.id, "accepted");
    }

    get meetingTime() {
        return serverToLocal(this.recommendation.eventTime);
    }

    get meetingHistory() {
        return (a: { q: string }) => Promise.resolve(this.findItem(this.pMeetingHistory, a.q));
    }

    get user(): IUser {
        return this.recommendation.recommendedCourseUser.user;
    }

    get location(): string {
        return this.recommendation.location;
    }
}
</script>
