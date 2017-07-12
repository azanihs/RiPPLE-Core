<template>
    <md-layout class="half">
        <h2>Engagement Overview</h2>
        <chart :type="'pie'"
               :data="data"
               :options="options"></chart>
    </md-layout>
</template>
<style scoped>
    h2 {
        width: 100%;
        padding-top: 0.75em;
    }
    
    .half {
        width: 50%;
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
            labels: ["Sleeping", "Designing", "Coding", "Cycling"],
            datasets: [{
                data: [20, 40, 5, 35],
                backgroundColor: [
                    "#1fc8db",
                    "#fce473",
                    "#42afe3",
                    "#ed6c63",
                    "#97cd76"
                ]
            }]
        };
        options = {
            segmentShowStroke: false
        };

    }
</script>
