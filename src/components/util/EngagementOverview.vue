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
        <md-layout md-gutter
                   md-flex="50">
            <div class="engagementScoreContainer">
                <h3>Engagement Score</h3>
                <div class="engagementScore">
                    <div class="engagementButton">
                        68
                    </div>
                    <md-spinner class="engagementScoreProgress"
                                :md-stroke="2"
                                :md-progress="68.95"></md-spinner>
                </div>
            </div>
        </md-layout>
    </md-layout>
</template>
<style scoped>
    h2 {
        width: 100%;
        padding-top: 0.75em;
    }
    
    .engagementScoreContainer {
        width: 100%;
    }
    
    h3 {
        display: inline-block;
        vertical-align: middle;
    }
    
    .engagementScore {
        position: relative;
        font-size: 1.5em;
        text-align: center;
        display: inline-block;
        vertical-align: middle;
        margin-left: 1em;
    }
    
    .engagementButton {
        padding: 0.25em;
        background-color: transparent !important;
        color: #256 !important;
    }
    
    .engagementScoreProgress {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
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

        get engagementScore() {
            return UserService.getEngagementBreakdown();
        }


    }
</script>
