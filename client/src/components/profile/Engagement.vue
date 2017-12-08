<template>
     <md-layout>
        <overview-description>
            <h2>Engagement Overview</h2>
            <p>The engagement overview will show you how your engagments with Ripple compare with the rest of your cohort</p>
        </overview-description>
        <variable-data-visualiser class="componentSeparator"
            chartType="radar"
            :allowedChartTypes="[{name: 'Radar Chart', value: 'radar'}]"
            :dataCategories="engagementItems"
            :compareList="generateEngagement">
        </variable-data-visualiser>
        <collected-badges topic='engagement'></collected-badges>
    </md-layout>
</template>


<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { ITopic } from "../../interfaces/models";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";

import CollectedBadges from "../util/CollectedBadges.vue";
import OverviewDescription from "../util/OverviewDescription.vue";
import VariableDataVisualiser from "../charts/VariableDataVisualiser.vue";

@Component({
    components: {
        VariableDataVisualiser,
        OverviewDescription,
        CollectedBadges
    }
})
export default class EngagementView extends Vue {

    pEngagementItems: ITopic[] = [];

    updateEngagementItems(newEngagementItems: ITopic[]) {
        this.pEngagementItems = newEngagementItems;
    };

    @Lifecycle
    created() {
        Fetcher.get(UserService.getAllAvailableEngagementTypes)
            .on(this.updateEngagementItems);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getAllAvailableEngagementTypes)
            .off(this.updateEngagementItems);
    }

    get engagementItems() {
        return this.pEngagementItems;
    }

    generateEngagement(_: any) {
        return UserService.getEngagementScores;
    }
}
</script>
