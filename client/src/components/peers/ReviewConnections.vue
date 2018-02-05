<template>
    <md-layout>
        <md-card class="fullWidth">
            <md-layout md-flex="100">
                <h2>Review Connections</h2>
                <md-layout md-flex="100"
                           md-gutter="16">
                    <md-layout md-flex="33"
                               md-gutter
                               class="componentSeparator"
                               v-for="(recommendation, i) in recommendations"
                               :key="i">
                        <recommendation-review-card :recommendation="recommendation">
                            Request
                        </recommendation-review-card>
                    </md-layout>
                </md-layout>
            </md-layout>
        </md-card>
    </md-layout>
</template>

<style>

    .connect-tabs .md-tabs-navigation-container {
        background-color: #4d656d;
    }

    .connect-tabs .md-tab-header {

        background-color: rgba(34,85,102, 0.7);
        border-bottom: 6px solid #f2f2f2;
    }

    .connect-tabs .md-tab-header:hover {
        background-color: rgba(34,85,102, 0.4);
    }

    .connect-tabs span {
        font-weight: bold;
        font-family: Verdana,Arial,Helvetica,sans-serif;
    }
    .connect-tabs .md-active span{
        color: #f2f2f2;
    }

    .connect-tabs .md-active {
        background-color: #256;
    }

    .connect-tabs .md-tab-indicator{
        background-color: #1d323a !important;
        height: 6px;
    }



</style>

<style scoped>
.tab {
    padding-left: 2px !important;
    padding-right: 2px !important;
}

.table {
    border: none;
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

.table tbody td:first-child {
    position: relative;
}

.table thead tr {
    background-color: #256;
    color: #f2f2f2;
}

.table tbody tr:nth-child(even) {
    background-color: #efefef;
}

.table tr td,
.table thead tr th {
    text-align: center;
    padding: 8px 0px;
}

.cellOverlay {
    position: absolute;
    left: 0px;
    top: 5%;
    width: 0px;
    height: 90%;
    border: 1px solid transparent;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { IRecommendation } from "../../interfaces/models";
import RecommendationService from "../../services/RecommendationService";
import Fetcher from "../../services/Fetcher";
import RecommendationReviewCard from "./RecommendationReviewCard.vue";

@Component({
    components: {
        RecommendationReviewCard
    }
})
export default class ReviewConnections extends Vue {

    pReviewRecommendations: IRecommendation[] = [];

    updateReviewRecommendations(recommendations: IRecommendation[]) {
        this.pReviewRecommendations = recommendations;
    };

    @Lifecycle
    created() {
        Fetcher.get(RecommendationService.reviewRecommendations)
            .on(this.updateReviewRecommendations);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(RecommendationService.reviewRecommendations)
            .off(this.updateReviewRecommendations);
    }

    get recommendations() {
        return this.pReviewRecommendations;
    }
}
</script>
