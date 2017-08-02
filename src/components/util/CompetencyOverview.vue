<template>
    <md-layout md-gutter="16" class="overview">
        <md-layout md-flex="75">
            <h4 class="chartHeader">Your Current Results vs. {{compare}}</h4>
            <div class="chartContainer">
                <div class="chartPanel">
                    <chart :type="chart" :data="competencies.data" :options="competencies.options"></chart>
                </div>
            </div>
        </md-layout>
        <md-layout md-flex="25">
            <div class="settingsContainer">
                <div class="visualisationMenu">
                    <h3>Change Visualisation Data</h3>
                    <md-input-container>
                        <label for="visualisationType">
                            Visualisation Type
                        </label>
                        <md-select name="visualisationType" id="visualisationType" v-model="chart">
                            <md-option value="bar">
                                <div class="chart barChart">Bar Chart</div>
                            </md-option>
                            <md-option value="radar">
                                <div class="chart pieChart">Pie Chart</div>
                            </md-option>
                        </md-select>
                    </md-input-container>
                    <md-input-container>
                        <label for="visulisationCompare">
                            Compare Data
                        </label>
                        <md-select name="visulisationCompare" id="visulisationCompare" v-model="compare">
                            <md-option value="Personal Goals">
                                Personal Goals
                            </md-option>
                            <md-option value="Peers">
                                Peers
                            </md-option>
                            <md-option value="Previous Offerings">
                                Previous Offerings
                            </md-option>
                        </md-select>
                    </md-input-container>
                    <h4>Topics to Visulise</h4>
                    <topic-chip v-for="topic in topics" :key="topic" :disabled="isDisabled(topic)" @click.native="toggleTopic(topic)">
                        {{topic}}
                    </topic-chip>
                </div>
            </div>
        </md-layout>
    </md-layout>
</template>
<style scoped>
.overview {
    justify-content: center;
    align-items: center;
    margin-bottom: 1em;
}

.chartContainer {
    width: 100%;
}

h3 {
    width: 100%;
}

.chartHeader {
    width: 100%;
    text-align: center;
    margin-top: 0px;
}

.chartPanel {
    display: block;
    width: 100%;
    height: 100%;
    position: relative;
}


.chart {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chart::before {
    font-family: 'Material Icons';
}

.barChart::before {
    content: "bar_chart";
}

.pieChart::before {
    content: "pie_chart";
}

.visualisationMenu {}

.visualisationMenu>h3 {
    margin-top: 0px;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import Chart from "../charts/Chart.vue";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";

import OverviewDescription from "./OverviewDescription.vue";
import TopicChip from "./TopicChip.vue";

@Component({
    components: {
        Chart,
        OverviewDescription,
        TopicChip
    }
})
export default class CompetencyOverview extends Vue {
    @Prop chartType = p({
        type: String,
        default: "bar"
    }) as string;

    pChartType: string = "";
    pCompareAgainst: string = "Personal Goals";
    hiddenTopics: string[] = [];

    get chart() {
        return this.pChartType || this.chartType;
    }
    set chart(newVal: string) {
        this.pChartType = newVal;
    }

    get compare() {
        return this.pCompareAgainst;
    }
    set compare(newVal: string) {
        this.pCompareAgainst = newVal;
    }

    get topics() {
        return TopicService.getAllAvailableTopics();
    }

    updateChart() {
        const dim = this.$el.querySelector(".visualisationMenu").getBoundingClientRect();
        this.$el.querySelector(".chartContainer")["style"].height = dim.height + "px";
    }

    @Lifecycle
    mounted() {
        this.updateChart();
        window.addEventListener("resize", this.updateChart);
    }

    @Lifecycle
    destroyed() {
        window.removeEventListener("resize", this.updateChart);
    }

    toggleTopic(topic) {
        const foundIndex = this.hiddenTopics.indexOf(topic);
        if (foundIndex >= 0) {
            this.hiddenTopics.splice(foundIndex, 1);
        } else {
            this.hiddenTopics.push(topic);
        }
    }

    isDisabled(topic) {
        return this.hiddenTopics.indexOf(topic) >= 0;
    }

    getColour(c) {
        if (c < 50) {
            return "rgba(255, 99, 132, ";
        } else if (c >= 50 && c <= 75) {
            return "rgba(255, 206, 86, ";
        } else {
            return "rgba(34, 85, 102, ";
        }
    };

    get competencies() {
        const topics = this.topics.filter(x => this.hiddenTopics.indexOf(x) == -1);

        const data = UserService.userCompetencies(topics);
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
                responsive: true,
                scale: {
                    ticks: {
                        beginAtZero: true
                    }
                }
            }
        };

        if (this.chart == "radar") {
            Object.assign(compareData, {
                type: "radar",
                pointStyle: "default",
                backgroundColor: "rgba(0, 0, 0, 0.4)",
                pointBorderColor: "rgba(0, 0, 0, 0.6)",
                pointBackgroundColor: "rgba(0, 0, 0, 0.6)"
            });
            Object.assign(chartData.options, {
                //responsive: false
            });
        }
        return chartData;
    }
}
</script>
