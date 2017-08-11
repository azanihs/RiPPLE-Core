<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100"
            class="componentSeparator">
            <h1>Availability</h1>
            <availability-selector @change="shuffleData(null)"></availability-selector>
        </md-layout>
        <md-layout md-flex="100">
            <md-card>
                <recommendation-search :searchTypes="searchTypes"
                    :generator="this.shuffleData"
                    :topics="topics"></recommendation-search>
            </md-card>
        </md-layout>
    </md-layout>
</template>

<style scoped>
h1 {
    width: 100%;
}

.md-tabs {
    border-top: 1px solid rgba(0, 0, 0, .12);
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";
import AvailabilitySelector from "../util/AvailabilitySelector.vue";
import RecommendationSearch from "./RecommendationSearch.vue";

@Component({
    components: {
        AvailabilitySelector,
        RecommendationSearch
    }
})
export default class PeerView extends Vue {

    searchTypes = ["Provide Mentorship", "Seek Mentorship", "Find Study Partners"];

    @Lifecycle
    created() {
        this.shuffleData("all");
    }

    get topics() {
        return TopicService.getAllAvailableTopics();
    }

    shuffleData(type: string) {
        return {
            recommendations: UserService.getRecommendedConnections(3),
            requests: UserService.getOutstandingRequests(3)
        };
    }
}
</script>
