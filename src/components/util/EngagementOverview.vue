<template>
    <md-layout md-gutter="16">
        <h2>Engagement Overview</h2>
        <md-layout md-gutter
                   md-flex="50">
            <chart :type="'pie'"
                   :data="data"
                   :options="options">
            </chart>
        </md-layout>
        <md-layout md-gutter
                   md-flex="50">
            <chart :type="'radar'"
                   :data="data"
                   :options="options"></chart>
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

    @Component({
        components: {
            "chart": Chart
        }
    })
    export default class EngagementOverview extends Vue {
        data = {
            labels: ["Running", "Swimming", "Eating", "Cycling"],
            datasets: [{
                data: [20, 10, 40, 10],
                label: "Your Score",
                backgroundColor: [
                    "rgba(255, 99, 132, 0.2)",
                    "rgba(54, 162, 235, 0.2)",
                    "rgba(255, 206, 86, 0.2)",
                    "rgba(75, 192, 192, 0.2)",
                    "rgba(153, 102, 255, 0.2)",
                    "rgba(255, 159, 64, 0.2)"
                ],
                borderColor: [
                    "rgba(255,99,132,1)",
                    "rgba(54, 162, 235, 1)",
                    "rgba(255, 206, 86, 1)",
                    "rgba(75, 192, 192, 1)",
                    "rgba(153, 102, 255, 1)",
                    "rgba(255, 159, 64, 1)"
                ]
            }]
        };
        options = {
            scale: {
                ticks: {
                    beginAtZero: true
                }
            },
            animation: {
                animateRotate: true
            }
        };
    }
</script>
