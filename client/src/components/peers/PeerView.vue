<template>
    <md-layout md-flex="100"
               class="topPadding">
        <md-layout md-flex="100"
                   class="componentSeparator">
            <availability-selector @change="changeAvailability"
                                   :course="course"
                                   :user="user"></availability-selector>
        </md-layout>
        <md-layout md-flex="100">
            <md-card>
                <recommendation-search @change="shuffleData()"
                                       :recommendations="recommendations"
                                       :requests="requests"
                                       :studyRoles="studyRoles"
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
import AvailabilityService from "../../services/AvailabilityService";
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
    pCourseAvailability = [];
    pUserAvailability = [];
    pStudyRoles = [];

    updateTopics(newTopics) {
        this.pTopics = newTopics;
    };
    updateConnections(newConnections) {
        this.pRecommendations = newConnections;
    };
    updateRequests(newRequests) {
        this.pRequests = newRequests;
    };
    updateCourseAvailability(availability) {
        this.pCourseAvailability = availability;
    };
    updateUserAvailability(availability) {
        this.pUserAvailability = availability;
    };
    updateStudyRoles(roles) {
        this.pStudyRoles = roles;
    }

    @Lifecycle
    created() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateTopics);
        UserService.getRecommendedConnections({ count: 3 })
            .then(this.updateConnections);
        UserService.getOutstandingRequests({ count: 3 })
            .then(this.updateRequests);
        AvailabilityService.getCourseAvailability()
            .then(this.updateCourseAvailability);
        AvailabilityService.getUserAvailability()
            .then(this.updateUserAvailability);
        AvailabilityService.getStudyRoles()
            .then(this.updateStudyRoles);
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

    get course() {
        return this.pCourseAvailability;
    }

    get user() {
        return this.pUserAvailability;
    }

    get studyRoles() {
        return this.pStudyRoles;
    }

    changeAvailability(day, time) {
        AvailabilityService.updateUserAvailability(day, time);
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
