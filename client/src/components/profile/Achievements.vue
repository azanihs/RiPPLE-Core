<template>
    <md-layout :class = "{ 'mobileStyleAchievements': mobileMode }">
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
    </md-layout>
</template>

<style scoped>

.componentSeparator{
    flex:auto !important;
}

.mobileStyleAchievements {
    min-width: 600px;
}

</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";

import CollectedBadges from "../util/CollectedBadges.vue";
import OverviewDescription from "../util/OverviewDescription.vue";
import ApplicationService from "../../services/ApplicationService";

@Component({
    components:{
        OverviewDescription,
        CollectedBadges
    }
})
export default class AchievementView extends Vue {

    mobileMode: boolean = false;

    @Lifecycle
    mounted() {
        this.mobileMode = ApplicationService.getMobileMode();
    }
}
</script>
