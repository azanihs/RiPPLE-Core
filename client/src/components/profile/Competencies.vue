<template>
    <md-layout>
        <overview-description>
            <h2>Competency Overview</h2>
            <p>The competency overview will show how your are progressing towards your goals</p>
        </overview-description>
        <variable-data-visualiser class="componentSeparator"
            :dataCategories="topics"
            :compareList="generateCompetencies">
        </variable-data-visualiser>
        <collected-badges topic='competencies'></collected-badges>
    </md-layout>
</template>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";

import { Topic } from "../../interfaces/models";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";

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
export default class CompetenciesView extends Vue {

    pTopics: Topic[] = [];

    updateTopics(topics: Topic[]) {
        this.pTopics = topics;
    };

    @Lifecycle
    created() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateTopics);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateTopics);
    }

    get topics() {
        return this.pTopics;
    }

    generateCompetencies() {
        return UserService.userCompetencies;
    }
}
</script>
