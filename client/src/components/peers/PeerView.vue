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
                <recommendation-search @change="changeRoles"
                                       :recommendations="recommendations"
                                       :requests="requests"
                                       :studyRoles="studyRoles"
                                       :topics="topics"
                                       :userRoles="userRoles"></recommendation-search>
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
import { Vue, Component, Lifecycle } from "av-ts";
import {
    IAvailableRole, IAvailability, ICourseAvailability, IDay, ITime, IStudyRole, ITopic, IUser
} from "../../interfaces/models";

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
    pTopics: ITopic[] = [];
    pRequests: IUser[] = [];
    pRecommendations: IUser[] = [];
    pCourseAvailability: ICourseAvailability[] = [];
    pUserAvailability: IAvailability[] = [];
    pDays: IDay[] = [];
    pTimes: ITime[] = [];
    pCourseDistribution: number[][] = [];
    pMaxAvailable: number = 0;
    pStudyRoles: IStudyRole[] = [];
    pUserAvailableRoles = new Map<string, Map<string, boolean>>();

    updateTopics(newTopics: ITopic[]) {
        this.pTopics = newTopics;
    };
    updateConnections(newConnections: IUser[]) {
        this.pRecommendations = newConnections;
    };
    updateRequests(newRequests: IUser[]) {
        this.pRequests = newRequests;
    };
    updateCourseAvailability(availability: ICourseAvailability[]) {
        this.pCourseAvailability = availability;
    };
    updateUserAvailability(availability: IAvailability[]) {
        this.pUserAvailability = availability;
    };
    updateDays(days: IDay[]) {
        this.pDays = days;
    };
    updateTimes(times: ITime[]) {
        this.pTimes = times;
    };

    updateAvailability(courseDistribution: ICourseAvailability[]) {
        let maxAvailable = 0;
        let distribution = new Array(7);
        for (let i = 0; i < distribution.length; i++) {
            distribution[i] = new Array(24).fill(0);
        }

        courseDistribution.forEach(entry => {
            distribution[entry.day - 1][entry.time - 1] = entry.entries;
            if (entry.entries > maxAvailable) {
                maxAvailable = entry.entries;
            }
        });
        this.pCourseDistribution = distribution;
        this.pMaxAvailable = maxAvailable;
    };

    updateStudyRoles(roles: IStudyRole[]) {
        this.pStudyRoles = roles;
    };

    updateUserAvailableRoles(availableRoles: IAvailableRole[]) {
        const userRoles = new Map<string, Map<string, boolean>>();
        availableRoles.map(role => {
            const topic: string = role.topic.name;
            const studyRole: string = role.studyRole.role;
            if (userRoles.has(topic)) {
                const topicRoles = userRoles.get(topic)!;
                topicRoles.set(studyRole, true);
            } else {
                const studyRoles = new Map<string, boolean>();
                studyRoles.set(studyRole, true);
                userRoles.set(topic, studyRoles);
            }
        });
        this.pUserAvailableRoles = userRoles;
    };

    @Lifecycle
    created() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateTopics);
        UserService.getRecommendedConnections({ count: 7 })
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
        Fetcher.get(AvailabilityService.getStudyRoles)
            .on(this.updateStudyRoles);
        Fetcher.get(AvailabilityService.getUserAvailableRoles)
            .on(this.updateUserAvailableRoles);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateTopics);
        Fetcher.get(AvailabilityService.getUserAvailability)
            .off(this.updateUserAvailability);
        Fetcher.get(AvailabilityService.getCourseAvailability)
            .off(this.updateAvailability);
        Fetcher.get(AvailabilityService.getStudyRoles)
            .off(this.updateStudyRoles);
        Fetcher.get(AvailabilityService.getUserAvailableRoles)
            .off(this.updateUserAvailableRoles);
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

    get studyRoles() {
        return this.pStudyRoles;
    }

    get userRoles() {
        return this.pUserAvailableRoles;
    }

    changeAvailability(day: number, time: number) {
        AvailabilityService.updateUserAvailability(day, time)
            .then(_ => AvailabilityService.getCourseAvailability())
            .then(x => this.updateCourseAvailability(x));
    }

    changeRoles(topic: number, studyRole: number) {
        AvailabilityService.updateUserRoles(topic, studyRole);
    }
}
</script>
