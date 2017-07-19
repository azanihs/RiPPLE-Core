<template>
    <md-layout>
        <overview-description>
            <h2>Question Recommendations</h2>
            <p>Have resources and exercises recommended to you in order to improve your course competencies</p>
        </overview-description>
        <h3>Current Competency Scores</h3>
        <md-layout md-flex="100"
                   class="competencyContainer">
            <chart type="bar"
                   :data="competencies.data"
                   :options="competencies.options"></chart>
        </md-layout>
        <question type="random"></question>
    </md-layout>
</template>

<style scoped>
    .competencyContainer {
        height: 10em;
        padding-bottom: 1em;
        border-bottom: 1px solid #ddd;
    }
    
    h3 {
        margin-top: 0px;
    }
    
    .chart {
        width: 100%;
    }
</style>


<script lang="ts">
    import { Vue, Component, Lifecycle, Prop } from "av-ts";
    import Chart from "../charts/Chart.vue";
    import Question from "../questions/Question.vue";
    import OverviewDescription from "../profile/OverviewDescription.vue";
    import UserService from "../../services/UserService";

    @Component({
        components: {
            "chart": Chart,
            "overview-description": OverviewDescription,
            "question": Question
        }
    })
    export default class QuestionRecommender extends Vue {

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
                            maxTicksLimit: 5,
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
