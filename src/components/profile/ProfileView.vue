<template>
    <md-layout>
        <md-tabs md-fixed class="md-transparent">
            <md-tab md-label="Overview">
                <md-layout md-flex="100" class="separator">
                    <md-layout md-flex="50">
                        g
                    </md-layout>
                    <md-layout md-flex="50">
                        <md-card class="card">
                            <div v-for="item in engagementSummary" :key="item.name" class="engagementItem">
                                <h3>{{item.name}}</h3>
                                <div class="engagementScore">
                                    <div class="engagementButton">
                                        {{item.score}}
                                    </div>
                                    <md-spinner md-theme="spinner" class="engagementScoreProgress" :md-stroke="2" :md-progress="100"></md-spinner>
                                    <md-spinner class="progressSpinner engagementScoreProgress" :md-stroke="2" :md-progress="item.score"></md-spinner>
                                </div>
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
                <variable-data-visualiser class="separator" :dataCategories="engagementItems" :compareList="generateEngagement">
                </variable-data-visualiser>
                <collected-badges topic='engagement'></collected-badges>
            </md-tab>
            <md-tab md-label="Competencies">
                <overview-description>
                    <h2>Competency Overview</h2>
                    <p>The competency overview will show how your are progressing towards your goals</p>
                </overview-description>
                <variable-data-visualiser class="separator" :dataCategories="topics" :compareList="generateCompetencies">
                </variable-data-visualiser>
                <collected-badges topic='competencies'></collected-badges>
            </md-tab>
            <md-tab md-label="Connections">
                <overview-description>
                    <h2>Connection Overview</h2>
                    <p>The connections overview will show you how you have connected to peers through Ripple.</p>
                </overview-description>
                <connectedness-heatmap class="separator" :data="profileData" :topics="topics" :categories="categories"></connectedness-heatmap>
                <connection-overview class="separator"></connection-overview>
                <collected-badges topic='connections'></collected-badges>
            </md-tab>
            <md-tab md-label="Achievements">
                <overview-description>
                    <h2>Achievement Overview</h2>
                    <p>The achievement overview tracks noteable feats you have accomplished in Ripple, and shows you your progress towards those you have not yet achieved.</p>
                </overview-description>
                <collected-badges class="separator" topic='closest'></collected-badges>
                <collected-badges class="separator" topic='engagement'></collected-badges>
                <collected-badges class="separator" topic='competencies'></collected-badges>
                <collected-badges topic='connections'></collected-badges>
            </md-tab>
        </md-tabs>
    </md-layout>
</template>

<style scoped>
.separator {
    margin-bottom: 2em;
}

.engagementItem {
    flex-grow: 1;
    width: 47.5%;
    padding: 1em;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #f9f9f9;
    margin-bottom: 2em;
    border: 1px solid #f2f2f2;
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
    display: inline-block;
    vertical-align: middle;
    width: 75%;
    margin: 0px;
}

.engagementScore {
    position: relative;
    text-align: center;
    display: inline-block;
    vertical-align: middle;
    right: 25px;
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
import { Vue, Component } from "av-ts";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";

import ConnectednessHeatmap from "../util/ConnectednessHeatmap.vue";
import VariableDataVisualiser from "../charts/VariableDataVisualiser.vue";
import ConnectionOverview from "./ConnectionOverview.vue";
import OverviewDescription from "../util/OverviewDescription.vue";
import CollectedBadges from "../util/CollectedBadges.vue";

@Component({
    components: {
        VariableDataVisualiser,
        ConnectionOverview,
        ConnectednessHeatmap,
        OverviewDescription,
        CollectedBadges
    }
})
export default class DefaultView extends Vue {

    get profileData() {
        return UserService.getLoggedInUser();
    }
    get topics() {
        return TopicService.getAllAvailableTopics();
    }

    get engagementItems() {
        return [
            "Competencies",
            "Goal Progress",
            "Achievements",
            "Recommendations Accepted",
            "Social Connections",
            "Study Partners",
            "Peers Mentored",
            "Questions Rated",
            "Questions Asked",
            "Questions Answered",
            "Questions Viewed"];
    }

    get engagementSummary() {
        const scores = UserService.getEngagementScores(this.engagementItems);
        return scores.topics.map((x, i) => ({
            name: x,
            score: scores.ownScore[i]
        }));
    }

    generateEngagement(itemsToInclude) {
        return UserService.getEngagementScores(itemsToInclude);
    }

    get categories() {
        // Mentoring types
        return UserService.getAllAvailableCategories();
    }

    generateCompetencies(itemsToInclude) {
        return UserService.userCompetencies(itemsToInclude);
    }

}
</script>
