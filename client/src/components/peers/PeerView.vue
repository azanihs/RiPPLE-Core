<template>
    <md-layout md-flex="100"
               class="topPadding">
        <md-layout md-flex="100"
                   class="componentSeparator">
            <availability-selector @change="changeAvailability"
                                   :days="days"
                                   :times="times"
                                   :courseDistribution="course"
                                   :userDistribution="user"
                                   :maxAvailable="maxAvailable"></availability-selector>
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
import { Availability, CourseAvailability, Day, Time } from "../../interfaces/models";

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
    pDays: Day[] = [];
    pTimes: Time[] = [];
    pCourseDistribution: number[][] = [];
    pMaxAvailable: number = 0;

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
    updateDays(days) {
        this.pDays = days;
    };
    updateTimes(times) {
        this.pTimes = times;
    };
    updateAvailability(courseDistribution) {
        let maxAvailable = 0;
        let distribution = new Array(7);
        for (let i =0; i < distribution.length; i++) {
            distribution[i] = new Array(24).fill(0);
        }
        courseDistribution.map(entry => {
            distribution[entry.day - 1][entry.time - 1] = entry.entries;
            if (entry.entries > maxAvailable) {
                maxAvailable = entry.entries;
            }
        });
        this.pCourseDistribution = distribution;
        this.pMaxAvailable = maxAvailable;
    };

    @Lifecycle
    created() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateTopics);
        UserService.getRecommendedConnections({ count: 3 })
            .then(this.updateConnections);
        UserService.getOutstandingRequests({ count: 3 })
            .then(this.updateRequests);

        Fetcher.get(AvailabilityService.getUserAvailability)
            .on(this.updateUserAvailability);

        Promise.all([
            AvailabilityService.getDays(),
            AvailabilityService.getUTCTimeSlots()
        ])
        .then(data => {
            this.updateDays(data[0]);
            this.updateTimes(data[1]);
        });

        Fetcher.get(AvailabilityService.getCourseAvailability)
            .on(this.updateAvailability);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateTopics);
        Fetcher.get(AvailabilityService.getUserAvailability)
            .off(this.updateUserAvailability);
        Fetcher.get(AvailabilityService.getCourseAvailability)
            .off(this.updateAvailability);
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

    get days() {
        if (this.pDays.length > 0) {
            const days = this.pDays.slice(0, 5);
            return days;
        } else {
            return this.pDays;
        }
    }

    get times() {
        if (this.pTimes) {
            const times = this.pTimes.slice(8, 21);
            return times;
        } else {
            return this.pTimes;
        }
    }

    get course() {
        return this.pCourseDistribution;
    }

    get user() {
        return this.pUserAvailability;
    }

    get maxAvailable() {
        return this.pMaxAvailable;
    }

    changeAvailability(day, time) {
        AvailabilityService.updateUserAvailability(day, time)
        .then(x => AvailabilityService.getCourseAvailability())
        .then(this.updateCourseAvailability);
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
