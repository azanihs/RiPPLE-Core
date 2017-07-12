<template>
    <md-layout md-gutter="16">
        <h2>Engagement Overview</h2>
    
        <md-layout md-gutter
                   md-flex="50">
            <h3>Activity Breakdown</h3>
            <chart :type="'pie'"
                   :data="pieChart.data"
                   :options="pieChart.options">
            </chart>
        </md-layout>
    </md-layout>
</template>
<style scoped>
    h2 {
        width: 100%;
        padding-top: 0.75em;
    }
</style>

<script lang="ts">
    import { Vue, Component, Prop } from "av-ts";
    import Chart from "../charts/Chart.vue";
    import UserService from "../../services/UserService";

    @Component({
        components: {
            "chart": Chart
        }
    })
    export default class EngagementOverview extends Vue {

        get pieChart() {
            return UserService.getEngagementBreakdown();
        }

    }
</script>
