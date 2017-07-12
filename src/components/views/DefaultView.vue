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
                <collected-badges topic='all'></collected-badges>
            </md-tab>
        </md-tabs>
    </md-layout>
</template>

<style scoped>
    h1 {
        width: 100%;
    }
</style>

<script lang="ts">
    import { Vue, Component } from "av-ts";
    import EngagementOverview from "../util/EngagementOverview.vue";
    import CompetencyOverview from "../util/CompetencyOverview.vue";
    import ConnectionOverview from "../util/ConnectionOverview.vue";
    import CollectedBadges from "../util/CollectedBadges.vue";

    @Component({
        components: {
            "engagement-overview": EngagementOverview,
            "competency-overview": CompetencyOverview,
            "connection-overview": ConnectionOverview,
            "collected-badges": CollectedBadges
        }
    })
    export default class DefaultView extends Vue {
    }
</script>
