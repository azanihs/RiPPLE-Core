<template>
    <md-layout md-flex="75">
        <slot></slot>
        <div class="chartContainer">
            <div class="chartPanel">
                <chart :type="chartType"
                    :data="data"
                    :options="options"></chart>
            </div>
        </div>
    </md-layout>
</template>

<style scoped>
.chartContainer {
    width: 100%;
}

.chartPanel {
    display: block;
    width: 100%;
    height: 100%;
    position: relative;
}
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";

export default class CompetencyOverview extends Vue {
    @Prop
    chartType = p({
        default: "bar",
        type: String
    }) as string;

    @Prop
    compare = p({
        required: true,
        type: String
    }) as string;

    @Prop
    dataGenerator = p({
        type: Function,
        required: true
    }) as Function;


    getColour(c) {
        if (c < 50) {
            return "rgba(255, 99, 132, ";
        } else if (c >= 50 && c <= 75) {
            return "rgba(255, 206, 86, ";
        } else {
            return "rgba(34, 85, 102, ";
        }
    };

    get chartData() {
        const data = this.dataGenerator();

        const ownScores = data.ownScore;
        const compareScores = data.compareAgainst;

        const ownData = {
            data: ownScores,
            label: "Your Results",
            backgroundColor: ownScores.map(x => this.getColour(x) + "0.4)"),
            borderColor: ownScores.map(x => this.getColour(x) + "1)"),
            borderWidth: 2
        };

        const compareData = {
            data: compareScores,
            label: this.compare,
            type: "line",
            pointStyle: "triangle",
            backgroundColor: "rgba(29, 50, 58, 0.6)",
            showLine: false,
            pointBorderColor: "rgba(29, 50, 58, 0.6)",
            pointBackgroundColor: "rgba(29, 50, 58, 0.6)"
        };

        const chartData = {
            data: {
                labels: data.topics,
                datasets: [ownData, compareData]
            },
            options: {
                scale: {
                    ticks: {
                        beginAtZero: true
                    }
                }
            }
        };

        if (this.chartType == "radar") {
            Object.assign(compareData, {
                type: "radar",
                pointStyle: "default",
                backgroundColor: "rgba(0, 0, 0, 0.4)",
                pointBorderColor: "rgba(0, 0, 0, 0.6)",
                pointBackgroundColor: "rgba(0, 0, 0, 0.6)"
            });
            Object.assign(ownData, {
                backgroundColor: ownData.backgroundColor[0],
                borderColor: ownData.borderColor[0]
            });
        }
        return chartData;
    }
}
</script>
