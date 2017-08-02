<template>
    <md-layout md-gutter="16">
        <overview-description>
            <h2>Competency Overview</h2>
            <p>The competency overview will show how your are progressing towards your goals</p>
        </overview-description>
        <md-layout md-flex="50">
            <div class="chartContainer">
                <chart :type="chart" :data="competencies.data" :options="competencies.options"></chart>
            </div>
        </md-layout>
        <md-layout md-flex="50">
            <div class="visulisationMenu">
                <h3>Change Visulisation Data</h3>
                <md-input-container>
                    <label for="visulisationType">
                        Visulisation Type
                    </label>
                    <md-select name="visulisationType" id="visulisationType" v-model="chart">
                        <md-option value="bar">
                            <div class="chart barChart">Bar Chart</div>
                        </md-option>
                        <md-option value="radar">
                            <div class="chart pieChart">Pie Chart</div>
                        </md-option>
                    </md-select>
                </md-input-container>
                <md-input-container>
                    <label for="visulisationType">
                        Visulisation Against
                    </label>
                    <md-select name="visulisationType" id="visulisationType" v-model="compare">
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
            </div>
        </md-layout>
    </md-layout>
</template>
<style scoped>
h3 {
    width: 100%;
}

.chartContainer {
    width: 75%;
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

.visulisationMenu {
    width: 100%;
}

.visulisationMenu>h3 {
    margin-top: 0px;
}
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import Chart from "../charts/Chart.vue";
import UserService from "../../services/UserService";
import OverviewDescription from "./OverviewDescription.vue";

@Component({
    components: {
        "chart": Chart,
        "overview-description": OverviewDescription
    }
})
export default class CompetencyOverview extends Vue {
    @Prop chartType = p({
        type: String,
        default: "bar"
    }) as string;

    pChartType: string = "";
    pCompareAgainst: string = "Personal Goals";

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
        const data = UserService.userCompetencies(this.compare);
        if (this.chart == "radar") {
            //data.data.datasets[1]["type"] = "radar";
            //data.data.datasets[1]["backgroundColor"] = "rgba(29, 50, 58, 0.6)";
            //data.data.datasets[1]["pointBorderColor"] = "rgba(29, 50, 58, 0.6)";
            //data.data.datasets[1]["pointBackgroundColor"] = "rgba(29, 50, 58, 0.2)";
        }

        const ownScores = data.ownScore;
        const chartData = {
            data: {
                labels: data.topics,
                datasets: [{
                    data: ownScores,
                    label: "Your Results",
                    backgroundColor: ownScores.map(x => this.getColour(x) + "0.4)"),
                    borderColor: ownScores.map(x => this.getColour(x) + "1)"),
                    borderWidth: 2
                }, {
                    data: data.compareAgainst,
                    label: this.compare,
                    type: "line",
                    pointStyle: "triangle",
                    backgroundColor: "rgba(29, 50, 58, 0.6)",
                    showLine: false,
                    pointBorderColor: "rgba(29, 50, 58, 0.6)",
                    pointBackgroundColor: "rgba(29, 50, 58, 0.6)"
                }]
            },
            options: {
                scale: {
                    ticks: {
                        beginAtZero: true
                    }
                },
                scales: {
                    xAxes: [{
                        stacked: false
                    }],
                    yAxes: [{
                        stacked: false
                    }]
                }
            }
        };
        return data;
    }
    get lineChart() {
        return UserService.getComparativeEngagementBreakdown();
    }
}
</script>
