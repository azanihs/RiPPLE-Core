<template>
    <md-layout>
        <overview-description>
            <h2>Question Recommendations</h2>
            <p>Have resources and exercises recommended to you in order to improve your course competencies</p>
        </overview-description>
        <md-layout md-flex="100"
                   class="competencyContainer">
            <chart type="bar"
                   :data="competencies.data"
                   :options="competencies.options"></chart>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .competencyContainer {
        margin-top: 1em;
        height: 75%;
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

        getBackgroundColor(value): ({ borderColor: string, backgroundColor: string }) {
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
            const competencies = UserService.userCompetenciesOverview();
            competencies.options = {
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            min: 0,
                            max: 100,
                            stacked: true
                        }
                    }]
                }
            };
            const dataset = competencies.data.datasets[0];
            dataset.data.forEach(x => {
                const colourProperties = this.getBackgroundColor(x);
                dataset.backgroundColor.push(colourProperties.backgroundColor);
                dataset.borderColor.push(colourProperties.borderColor);
            });

            return competencies;
        }
    }
</script>
