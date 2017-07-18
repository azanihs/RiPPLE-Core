<template>
    <md-layout>
        <h1>Profile</h1>
        <md-tabs md-fixed
                 class="md-transparent">
            <md-tab md-label="Engagement">
                <engagement-overview></engagement-overview>
                <collected-badges topic='engagement'></collected-badges>
            </md-tab>
            <md-tab md-label="Competencies">
                <competency-overview></competency-overview>
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
                <!-- TODO: Align properly -->
                <collected-badges topic='engagement'></collected-badges>
                <collected-badges topic='competencies'></collected-badges>
                <collected-badges topic='connections'></collected-badges>
            </md-tab>
        </md-tabs>
    </md-layout>
</template>

<style scoped>
    
</style>

<script lang="ts">
    import { Vue, Component } from "av-ts";
    import EngagementOverview from "./EngagementOverview.vue";
    import CompetencyOverview from "./CompetencyOverview.vue";
    import ConnectionOverview from "./ConnectionOverview.vue";
    import OverviewDescription from "./OverviewDescription.vue";
    import CollectedBadges from "../util/CollectedBadges.vue";

    @Component({
        components: {
            "engagement-overview": EngagementOverview,
            "competency-overview": CompetencyOverview,
            "connection-overview": ConnectionOverview,
            "overview-description": OverviewDescription,
            "collected-badges": CollectedBadges
        }
    })
    export default class DefaultView extends Vue {
    }
</script>
