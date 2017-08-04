<template>
    <md-layout>
        <md-tabs md-fixed class="md-transparent">
            <md-tab md-label="Engagement">
                <overview-description>
                    <h2>Engagement Overview</h2>
                    <p>The engagement overview will show you how your engagments with Ripple compare with the rest of your cohort</p>
                </overview-description>
                <engagement-overview class="separator"></engagement-overview>
                <collected-badges topic='engagement'></collected-badges>
            </md-tab>
            <md-tab md-label="Competencies">
                <overview-description>
                    <h2>Competency Overview</h2>
                    <p>The competency overview will show how your are progressing towards your goals</p>
                </overview-description>
                <competency-overview class="separator"></competency-overview>
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
</style>

<script lang="ts">
import { Vue, Component } from "av-ts";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";

import ConnectednessHeatmap from "../util/ConnectednessHeatmap.vue";
import EngagementOverview from "./EngagementOverview.vue";
import CompetencyOverview from "../util/CompetencyOverview.vue";
import ConnectionOverview from "./ConnectionOverview.vue";
import OverviewDescription from "../util/OverviewDescription.vue";
import CollectedBadges from "../util/CollectedBadges.vue";

@Component({
    components: {
        EngagementOverview,
        CompetencyOverview,
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

    get categories() {
        return UserService.getAllAvailableCategories();
    }
}
</script>
