<template>
    <md-card class="card">
        <md-layout>
            <md-layout md-flex="50">
                <h3>Activity Breakdown</h3>
                <div class="pieChart">
                    <chart :type="'pie'" :data="pieChart.data" :options="pieChart.options">
                    </chart>
                </div>
            </md-layout>
            <md-layout md-flex="50">
                <div class="engagementScoreContainer">
                    <div v-for="item in engagementItems" :key="item.name" class="engagementItem">
                        <h3>{{item.name}}</h3>
                        <div class="engagementScore">
                            <div class="engagementButton">
                                {{item.score}}
                            </div>
                            <md-spinner md-theme="spinner" class="engagementScoreProgress" :md-stroke="2" :md-progress="100"></md-spinner>
                            <md-spinner class="engagementScoreProgress" :md-stroke="2" :md-progress="item.score"></md-spinner>
                        </div>
                    </div>
                </div>
            </md-layout>
        </md-layout>
    </md-card>
</template>
<style scoped>
.card {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    flex: 1;
    padding: 16px;
}

.engagementScoreContainer {
    width: 100%;
    display: flex;
    flex-flow: row wrap;
}

.engagementItem {
    flex-grow: 1;
    width: 47.5%;
    padding: 1em;
    display: flex;
    align-items: center;
    justify-content: space-between;

    background-color: #f9f9f9;
    margin-bottom: 2em;
    border: 1px solid #f2f2f2;
}

.engagementItem:nth-child(odd) {
    margin-right: 2.5%;
}

.engagementItem:nth-child(even) {
    margin-left: 2.5%;
}


h3 {
    width: 100%;
}


.engagementItem h3 {
    display: inline-block;
    vertical-align: middle;
    width: 75%;
    margin: 0px;
}

.pieChart {
    width: 75%;
}

.engagementScore {
    position: relative;
    text-align: center;
    display: inline-block;
    vertical-align: middle;
    right: 25px;
}

.engagementButton {
    font-size: 1.5em;
    background-color: transparent !important;
    color: #256 !important;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
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
import OverviewDescription from "../util/OverviewDescription.vue";

@Component({
    components: {
        "chart": Chart,
        "overview-description": OverviewDescription
    }
})
export default class EngagementOverview extends Vue {

    get pieChart() {
        const data = UserService.getEngagementBreakdown();
        data.options = {
            scale: {
                ticks: {
                    beginAtZero: true
                }
            },
            animation: {
                animateRotate: true
            },
            legend: {
                // https://github.com/chartjs/Chart.js/issues/3175
                position: "left",
                labels: {
                    fontSize: 12
                }
            }
        };
        return data;
    }

    get engagementItems() {
        return UserService.getEngagementScores();
    }

}
</script>
