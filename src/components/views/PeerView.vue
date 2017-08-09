<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100"
                   class="headingContainer">
            <h1>Availability</h1>
            <availability-selector @change="shuffleData(null)"></availability-selector>
        </md-layout>
        <md-layout md-flex="100">
            <recommendation-search :searchTypes="searchTypes"
                                   :generator="this.shuffleData"
                                   :topics="topics"></recommendation-search>
        </md-layout>
        <!--<md-layout class="fullHeight"
                                                       md-flex="100">
                                                <md-tabs md-fixed
                                                         class="md-transparent"
                                                         @change="tabChange">
                                                    <md-tab v-for="tab in tabLookup"
                                                            :key="tab.name"
                                                            :md-label="tab.name">
                                                        <recommendations @change="shuffleData(tab.name)"
                                                                         :tabName="tab.heading"
                                                                         :peers="tab.data"
                                                                         :threshold="tab.name == 'Provide Mentorship' ? 75 : 0"></recommendations>
                                                    </md-tab>
                                                </md-tabs>
                                            </md-layout>-->
    </md-layout>
</template>

<style scoped>
h1 {
    width: 100%;
}

.headingContainer {
    margin: 8px 0px 0px 0px;
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
