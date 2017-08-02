<template>
    <md-layout>
        <h1>Profile</h1>
        <md-tabs md-fixed class="md-transparent">
            <md-tab md-label="Engagement">
                <engagement-overview></engagement-overview>
                <collected-badges topic='engagement'></collected-badges>
            </md-tab>
            <md-tab md-label="Competencies">
                <overview-description>
                    <h2>Competency Overview</h2>
                    <p>The competency overview will show how your are progressing towards your goals</p>
                </overview-description>
                <competency-overview class="competencyOverview"></competency-overview>
                <collected-badges topic='competencies'></collected-badges>
            </md-tab>
            <md-tab md-label="Connections">
                <connection-overview></connection-overview>
                <collected-badges topic='connections'></collected-badges>
            </md-tab>
            <md-tab md-label="Achievements">
                <overview-description>
                    <h2>Achievement Overview</h2>
                    <p>The achievement overview tracks noteable feats you have accomplished in Ripple, and shows you your progress towards those you have not yet achieved.</p>
                </overview-description>
                <collected-badges :separator="false" topic='engagement'></collected-badges>
                <collected-badges topic='competencies'></collected-badges>
                <collected-badges topic='connections'></collected-badges>
            </md-tab>
        </md-tabs>
    </md-layout>
</template>

<style scoped>
.competencyOverview {
    min-height: 500px;
}
</style>

<script lang="ts">
import { Vue, Component } from "av-ts";
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
        OverviewDescription,
        CollectedBadges
    }
})
export default class DefaultView extends Vue {
}
</script>
