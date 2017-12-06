<template>
    <md-layout md-label="Connections">
        <overview-description>
            <h2>Connection Overview</h2>
            <p>The connections overview will show you how you have connected to peers through Ripple.</p>
        </overview-description>
        <connectedness-heatmap class="componentSeparator"
            :topics="topics"
            :categories="mentoringTypes"></connectedness-heatmap>
        <connection-overview class="componentSeparator"></connection-overview>
        <collected-badges topic='connections'></collected-badges>
    </md-layout>
</template>

<style scoped>

.componentSeparator{
    flex:auto !important;
}

</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { Topic } from "../../interfaces/models";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";
import CollectedBadges from "../util/CollectedBadges.vue";
import ConnectednessHeatmap from "../util/ConnectednessHeatmap.vue";
import ConnectionOverview from "./ConnectionOverview.vue";
import OverviewDescription from "../util/OverviewDescription.vue";

@Component({
    components:{
        ConnectionOverview,
        ConnectednessHeatmap,
        OverviewDescription,
        CollectedBadges
    }
})
export default class ConnectionsView extends Vue {

    pTopics: Topic[] = [];
    pMentoringTypes: string[] = [];

    updateMentoringTypes(newMentoringTypes: string[]) {
        this.pMentoringTypes = newMentoringTypes;
    };

    updateTopics(topics: Topic[]) {
        this.pTopics = topics;
    };

    @Lifecycle
    created() {
        Fetcher.get(UserService.getAllAvailableCategories)
            .on(this.updateMentoringTypes);
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateTopics);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getAllAvailableCategories)
            .off(this.updateMentoringTypes);
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateTopics);
    }

    get topics() {
        return this.pTopics;
    }

    get mentoringTypes() {
        return this.pMentoringTypes;
    }

}
</script>
