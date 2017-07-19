<template>
    <md-layout>
        <overview-description>
            <h2>Question Recommendations</h2>
            <p>Have resources and exercises recommended to you in order to improve your course competencies</p>
        </overview-description>
        <md-layout md-flex="100"
                   class="competencyContainer">
            <div v-for="chart in competencies"
                 :key="chart"
                 class="chart">
                <chart type="bar"
                       :data="chart.data"
                       :options="chart.options"></chart>
            </div>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .competencyContainer {
        margin-top: 1em;
    }
    
    .chart {
        flex: 1;
    }
</style>


<script lang="ts">
    import { Vue, Component, Lifecycle, Prop } from "av-ts";
    import Chart from "../charts/Chart.vue";
    import OverviewDescription from "../profile/OverviewDescription.vue";
    import UserService from "../../services/UserService";

    @Component({
        components: {
            "chart": Chart,
            "overview-description": OverviewDescription
        }
    })
    export default class Question extends Vue {

        getBackgroundColor(value): Object {
            if (value <= 25) {
                return {
                    backgroundColor: "rgba(208, 82, 82, 0.5)",
                    borderColor: "rgba(208, 82, 82, 1)"
                };
            } else if (value > 25 && value <= 50) {
                return {
                    backgroundColor: "rgba(220, 143, 9, 0.5)",
                    borderColor: "rgba(220, 143, 9, 1)"
                };
            } else if (value > 50 && value <= 75) {
                return {
                    backgroundColor: "rgba(34, 85, 102, 0.5)",
                    borderColor: "rgba(34, 85, 102, 1)"
                };
            }
            return {
                backgroundColor: "rgba(34, 85, 102, 0.85)",
                borderColor: "rgba(34, 85, 102, 1)"
            };
        }

        get competencies() {
            const data = UserService.userCompetencies().data;
            const options = UserService.userCompetencies().options;

            const userScores = data.datasets[1].data;

            return userScores.map((x, i) => ({
                data: {
                    labels: [data.labels[i]],
                    datasets: [{
                        data: [x],
                        label: "Your Qualification",
                        borderWidth: 1,
                        ...this.getBackgroundColor(x)
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: 100,
                                maxTicksLimit: 5
                            }
                        }]
                    },
                    legend: {
                        display: false
                    }
                }
            }));
        }
    }
</script>
