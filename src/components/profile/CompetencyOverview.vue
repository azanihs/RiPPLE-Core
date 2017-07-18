<template>
    <md-layout md-gutter="16">
        <overview-description>
            <h2>Competency Overview</h2>
            <p>The competency overview will show how your are progressing towards your goals</p>
        </overview-description>
        <md-layout md-flex="50">
            <h3>Goal Overview</h3>
            <div class="chartContainer">
                <chart :type="'bar'"
                       :data="competencies.data"
                       :options="competencies.options"></chart>
            </div>
        </md-layout>
        <md-layout md-flex="50">
            <h3>Results Overview</h3>
            <div class="chartContainer">
                <chart :type="'radar'"
                       :data="lineChart.data"
                       :options="lineChart.options"></chart>
            </div>
        </md-layout>
    </md-layout>
</template>
<style scoped>
    h3 {
        width: 100%;
    }
    
    .chartContainer {
        width: 75%;
    }
</style>

<script lang="ts">
    import { Vue, Component, Prop } from "av-ts";
    import Chart from "../charts/Chart.vue";
    import UserService from "../../services/UserService";
    import OverviewDescription from "./OverviewDescription.vue";

    @Component({
        components: {
            "chart": Chart,
            "overview-description": OverviewDescription
        }
    })
    export default class CompetencyOverview extends Vue {

        get competencies() {
            return UserService.userCompetencies();
        }
        get lineChart() {
            return UserService.getComparativeEngagementBreakdown();
        }
    }
</script>
