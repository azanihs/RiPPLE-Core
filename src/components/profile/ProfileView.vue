<template>
    <md-layout>
        <md-tabs md-fixed
                 class="md-transparent">
            <md-tab md-label="Overview">
                <md-layout md-flex="100"
                           class="componentSeparator overview">
                    <md-layout class="notificationSummary">
                        <h2>Notifications</h2>
                    </md-layout>
                    <md-layout class="engagementSummary">
                        <h2>Engagement</h2>
                    </md-layout>

                    <md-layout class="notificationSummary">
                        <notifications :showCount="5"></notifications>
                    </md-layout>
                    <md-layout class="engagementSummary">
                        <md-card v-for="item in engagementSummary"
                                 :key="item.node.id"
                                 class="engagementItem">
                            <h3>{{item.node.name}}</h3>
                            <div class="engagementScore">
                                <div class="engagementButton">
                                    {{item.score}}
                                </div>
                                <md-spinner md-theme="spinner"
                                            class="engagementScoreProgress"
                                            :md-stroke="2"
                                            :md-progress="100"></md-spinner>
                                <md-spinner class="progressSpinner engagementScoreProgress"
                                            :md-stroke="2"
                                            :md-progress="item.score"></md-spinner>
                            </div>
                        </md-card>
                    </md-layout>
                </md-layout>
                <collected-badges topic='closest'></collected-badges>
            </md-tab>
            <md-tab md-label="Engagement">
                <overview-description>
                    <h2>Engagement Overview</h2>
                    <p>The engagement overview will show you how your engagments with Ripple compare with the rest of your cohort</p>
                </overview-description>
                <variable-data-visualiser class="componentSeparator"
                                          :dataCategories="engagementItems"
                                          :compareList="generateEngagement">
                </variable-data-visualiser>
                <collected-badges topic='engagement'></collected-badges>
            </md-tab>
            <md-tab md-label="Competencies">
                <overview-description>
                    <h2>Competency Overview</h2>
                    <p>The competency overview will show how your are progressing towards your goals</p>
                </overview-description>
                <variable-data-visualiser class="componentSeparator"
                                          :dataCategories="topics"
                                          :compareList="generateCompetencies">
                </variable-data-visualiser>
                <collected-badges topic='competencies'></collected-badges>
            </md-tab>
            <md-tab md-label="Connections">
                <overview-description>
                    <h2>Connection Overview</h2>
                    <p>The connections overview will show you how you have connected to peers through Ripple.</p>
                </overview-description>
                <connectedness-heatmap class="componentSeparator"
                                       :connections="userConnections"
                                       :topics="topics"
                                       :categories="mentoringTypes"></connectedness-heatmap>
                <connection-overview class="componentSeparator"></connection-overview>
                <collected-badges topic='connections'></collected-badges>
            </md-tab>
            <md-tab md-label="Achievements">
                <overview-description>
                    <h2>Achievement Overview</h2>
                    <p>The achievement overview tracks noteable feats you have accomplished in Ripple, and shows you your progress towards those you have not yet achieved.</p>
                </overview-description>
                <collected-badges class="componentSeparator"
                                  topic='closest'></collected-badges>
                <collected-badges class="componentSeparator"
                                  topic='engagement'></collected-badges>
                <collected-badges class="componentSeparator"
                                  topic='competencies'></collected-badges>
                <collected-badges topic='connections'></collected-badges>
            </md-tab>
            <md-tab md-label="Notifications">
                <overview-description>
                    <h2>Notifications Overview</h2>
                    <p>The notifications overview shows you things which require your attention or action</p>
                </overview-description>
                <notifications></notifications>
            </md-tab>
        </md-tabs>
    </md-layout>
</template>

<style scoped>
.overview {
    align-items: flex-start;
}

.notificationSummary {
    align-items: flex-start;
    min-width: 48.75%;
    flex: 0 1 48.75%;
}

.engagementSummary {
    align-items: flex-start;
    min-width: 48.75%;
    flex: 0 1 48.75%;
    margin-left: 2.5%
}

h2 {
    width: 100%;
}

.engagementItem {
    flex: none !important;
    width: 47.5%;
    padding: 1em;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #f9f9f9;
    margin-bottom: 2em;
    border: 1px solid #f2f2f2;
    overflow: hidden;
}

.engagementItem:nth-child(odd) {
    margin-right: 2.5%;
}

.engagementItem:nth-child(even) {
    margin-left: 2.5%;
}

h3 {
    width: 100%;
}

.engagementItem h3 {
    display: block;
    width: 100%;
    margin: 0px 0px 0.5em 0px;
    text-align: center;
}

.engagementScore {
    position: relative;
    text-align: center;
    left: 50%;
    height: 50px;
}

.engagementScore::after {
    content: "\00a0";
}

.engagementButton {
    font-size: 1.5em;
    background-color: transparent !important;
    color: #256 !important;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.engagementScoreProgress {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";

import CollectedBadges from "../util/CollectedBadges.vue";
import ConnectednessHeatmap from "../util/ConnectednessHeatmap.vue";
import ConnectionOverview from "./ConnectionOverview.vue";
import Notifications from "../util/Notifications.vue";
import OverviewDescription from "../util/OverviewDescription.vue";
import VariableDataVisualiser from "../charts/VariableDataVisualiser.vue";

@Component({
    components: {
        VariableDataVisualiser,
        ConnectionOverview,
        ConnectednessHeatmap,
        OverviewDescription,
        Notifications,
        CollectedBadges
    }
})
export default class DefaultView extends Vue {

    pTopics = [];
    pUser = undefined;
    pEngagementItems = [];
    pEngagementSummary = [];
    pMentoringTypes = [];

    updateEngagementSummary(newSummary) {
        this.pEngagementSummary = newSummary;
    };
    updateEngagementItems(newEngagementItems) {
        this.pEngagementItems = newEngagementItems;
    };
    updateMentoringTypes(newMentoringTypes) {
        this.pMentoringTypes = newMentoringTypes;
    };
    updateUser(user) {
        this.pUser = user;
    };
    updateTopics(topics) {
        this.pTopics = topics;
    };

    @Lifecycle
    created() {
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateUser);
        Fetcher.get(UserService.getAllAvailableEngagementTypes)
            .on(this.updateEngagementItems);
        Fetcher.get(UserService.getAllAvailableCategories)
            .on(this.updateMentoringTypes);
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateTopics);
        Fetcher.get(UserService.getEngagementSummary)
            .on(this.updateEngagementSummary);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateUser);
        Fetcher.get(UserService.getAllAvailableEngagementTypes)
            .off(this.updateEngagementItems);
        Fetcher.get(UserService.getAllAvailableCategories)
            .off(this.updateMentoringTypes);
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateTopics);
        Fetcher.get(UserService.getEngagementSummary)
            .off(this.updateEngagementSummary);
    }

    get profileData() {
        return this.pUser;
    }

    get userConnections() {
        if (this.pUser !== undefined) {
            return this.pUser.connections;
        }
        return [];
    }

    get topics() {
        return this.pTopics;
    }

    get engagementItems() {
        return this.pEngagementItems;
    }

    get engagementSummary() {
        return this.pEngagementSummary;
    }

    generateEngagement(itemsToInclude) {
        return UserService.getEngagementScores;
    }

    get mentoringTypes() {
        return this.pMentoringTypes;
    }

    generateCompetencies(itemsToInclude) {
        return UserService.userCompetencies;
    }

}
</script>
