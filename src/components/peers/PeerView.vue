<template>
    <md-layout md-flex="100"
               class="topPadding">
        <md-layout md-flex="100"
                   class="componentSeparator">
            <availability-selector @change="shuffleData()"></availability-selector>
        </md-layout>
        <md-layout md-flex="100">
            <md-card>
                <recommendation-search @change="shuffleData()"
                                       :searchTypes="searchTypes"
                                       :recommendations="recommendations"
                                       :requests="requests"
                                       :topics="topics"></recommendation-search>
            </md-card>
        </md-layout>
    </md-layout>
</template>

<style scoped>
.topPadding {
    padding-top: 16px;
}

.md-tabs {
    border-top: 1px solid rgba(0, 0, 0, .12);
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Watch } from "av-ts";

import TopicService from "../../services/TopicService";
import UserService from "../../services/UserService";
import Fetcher from "../../services/Fetcher";

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
    pTopics = [];
    pRequests = [];
    pRecommendations = [];

    updateTopics(newTopics) {
        this.pTopics = newTopics;
    };
    updateConnections(newConnections) {
        this.pRecommendations = newConnections;
    };
    updateRequests(newRequests) {
        this.pRequests = newRequests;
    };

    @Lifecycle
    created() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateTopics);
        UserService.getRecommendedConnections({ count: 3 })
            .then(this.updateConnections);
        UserService.getOutstandingRequests({ count: 3 })
            .then(this.updateRequests);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateTopics);
    }

    get topics() {
        return this.pTopics;
    }

    get recommendations() {
        return this.pRecommendations;
    }
    get requests() {
        return this.pRequests;
    }

    shuffleData() {
        Promise.all([
            UserService.getRecommendedConnections({ count: 3 }),
            UserService.getOutstandingRequests({ count: 3 })
        ])
            .then(data => {
                this.updateConnections(data[0]);
                this.updateRequests(data[1]);
            });
    }
}
</script>
