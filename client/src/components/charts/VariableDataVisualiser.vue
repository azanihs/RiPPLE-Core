<template>
    <md-layout md-flex="100">
        <md-card class="fullWidth">
            <md-layout md-flex="100">
                <md-layout md-flex="75"
                    class="leftPanel">
                    <h2 class="chartHeader">Your Current Results vs. {{compare}}</h2>
                    <div class="chartContainer">
                        <div class="chartPanel">
                            <chart v-if="chartData"
                                ref="chart"
                                :type="chart"
                                :data="chartData.data"
                                :options="chartData.options"></chart>
                        </div>
                    </div>
                </md-layout>
                <md-layout md-flex="25"
                    class="rightPanel">
                    <div class="settingsContainer">
                        <div class="visualisationMenu">
                            <h3>Change Visualisation Data</h3>
                            <md-input-container>
                                <label for="visualisationType">
                                    Visualisation Type
                                </label>
                                <md-select name="visualisationType"
                                    id="visualisationType"
                                    v-model="chart">
                                    <md-option v-for="option in allowedChartTypes"
                                        :key="option.value"
                                        :value="option.value">
                                        <div :class="getChartClass(option.value)">{{option.name}}</div>
                                    </md-option>
                                </md-select>
                            </md-input-container>
                            <md-input-container>
                                <label for="visulisationCompare">
                                    Compare Data
                                </label>
                                <md-select name="visulisationCompare"
                                    id="visulisationCompare"
                                    v-model="compare">
                                    <md-option value="personalGoals">
                                        Personal Goals
                                    </md-option>
                                    <md-option value="peers">
                                        Peers
                                    </md-option>
                                    <md-option value="previousOfferings">
                                        Previous Offerings
                                    </md-option>
                                </md-select>
                            </md-input-container>
                            <h4>Topics to Visualise</h4>
                            <topic-chip v-for="category in dataCategories"
                                :key="category.id"
                                :disabled="isDisabled(category)"
                                @click.native="toggleVisible(category)">
                                {{category.name}}
                            </topic-chip>
                        </div>
                    </div>
                </md-layout>
            </md-layout>
        </md-card>
    </md-layout>
</template>

<style scoped>
.fullWidth {
    width: 100%;
    user-select: none;
    padding: 0px !important;
    overflow: hidden;
}

.leftPanel {
    padding: 16px;
    border: 1px solid #ddd;
    border-right-width: 0px;
}

.rightPanel {
    padding: 16px;
    background-color: #fafafa;
    color: #777;
    border: 1px solid #ddd;
    height: 100%;
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
    color: #999;
}

.chartPanel {
    display: block;
    width: 100%;
    height: 100%;
    position: relative;
}

.chartOption {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chartOption::before {
    font-family: "Material Icons";
    margin-right: 5px;
}

.barChart::before {
    content: "\E01D";
}

.radarChart::before {
    content: "\E1B3";
}

.topicDependency::before {
    content: "\E8C3";
}

.settingsContainer {
    margin: auto;
}

.visualisationMenu > h3 {
    margin-top: 0px;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Watch, Prop, p } from "av-ts";
import { Topic, Edge } from "../../interfaces/models";
import Fetcher from "../../services/Fetcher";

import TopicChip from "../util/TopicChip.vue";
import Chart from "./Chart.vue";

interface IChartType {
    name: string,
    value: string
};

@Component({
    components: {
        Chart,
        TopicChip
    }
})
export default class VariableDataVisualiser extends Vue {
    @Prop
    dataCategories = p<Topic[]>({
        required: true
    });

    // Subscribable function to provide access to dataset for chartType
    @Prop
    compareList = p<Function>({
        required: true
    });

    @Prop
    allowedChartTypes = p<IChartType[]>({
        required: false,
        default: () => [{
            name: "Bar Chart",
            value: "bar"
        }, {
            name: "Radar Chart",
            value: "radar"
        }, {
            name: "Topic Dependency Chart",
            value: "topicDependency"
        }]
    });

    @Prop
    chartType = p<string>({
        default: "bar"
    });

    pDataGeneratorFunction: Function | undefined = undefined;
    pChartData: any = {
        data: undefined,
        options: undefined
    };

    hiddenData: {[topicId: number]: boolean} = {};
    pChartType: string = "";
    pExcludeTopics: number[] = [];

    pCompareAgainst: string = "peers";

    get chart() {
        return this.pChartType || this.chartType;
    }

    set chart(newVal: string) {
        Fetcher.get(this.pDataGeneratorFunction as any,
            { compareTo: this.compare, exclude: this.pExcludeTopics })
            .off(this.updateChartData);

        this.pChartType = newVal;
        this.pChartData = undefined;
        this.pExcludeTopics = this.dataCategories.filter(x => this.isDisabled(x)).map(x => x.id);

        // Register this.compareList with the event bus to ensure synchrocity with the rest of the app
        Fetcher.get(this.pDataGeneratorFunction as any,
            { compareTo: this.compare, exclude: this.pExcludeTopics })
            .on(this.updateChartData);
    }

    get compare() {
        return this.pCompareAgainst;
    }

    set compare(newVal: string) {
        this.pCompareAgainst = newVal;
        this.chart = this.chart;
    }

    toggleVisible(dataItem: Topic) {
        if (this.hiddenData[dataItem.id]) {
            // this.hiddenData[dataItem.id] = false;
            this.$set(this.hiddenData as any, dataItem.id, false);
        } else {
            // this.hiddenData[dataItem.id] = true;
            this.$set(this.hiddenData as any, dataItem.id, true);
        }

        const topicsToShow = this.dataCategories.filter(x => !this.isDisabled(x));
        this.chart = this.chart;
        this.$emit("changeTopics", topicsToShow);
    }

    updateChart() {
        const dim = this.$el.querySelector(".visualisationMenu")!.getBoundingClientRect();
        const chartContainer = this.$el.querySelector(".chartContainer")! as HTMLDivElement;
        chartContainer.style.height = dim.height + "px";
    }

    calculateChartValues(newData: { topics: Topic[], ownScores: Edge[], compareAgainst: Edge[] }) {
        const { topics, ownScores, compareAgainst } = newData;

        let compareResults: any[];
        let ownResults: any[];
        let dataTopics: any[];

        if (this.chart != "topicDependency") {
            // Get all self loops from edge list, and use that competency.
            const findOrEmpty = (x: Topic) => (search: Edge[]) => {
                return search.find(s => s.source === x && s.target === x) || {
                    target: x,
                    source: x,
                    competency: 5,
                    attempts: 0
                };
            };
            compareResults = newData.topics.map(topic => findOrEmpty(topic)(compareAgainst)).map(x => x.competency);
            ownResults = newData.topics.map(topic => findOrEmpty(topic)(ownScores)).map(x => x.competency);
            dataTopics = newData.topics.map(x => x.name);
        } else {
            compareResults = compareAgainst.map(x => x);
            ownResults = ownScores.map(x => x);
            dataTopics = topics;
        }

        const ownData = {
            data: ownResults,
            label: "Your Results",
            backgroundColor: ownResults.map(x => this.getColour(x) + "0.4)"),
            borderColor: ownResults.map(x => this.getColour(x) + "1)"),
            borderWidth: 2
        };

        const compareData = {
            data: compareResults,
            label: this.compare,
            type: "line",
            showLine: true,

            backgroundColor: "rgba(245, 245, 245, 0.6)",
            pointBorderColor: compareResults.map(x => this.getColour(x) + "0.4)"),
            pointBackgroundColor: compareResults.map(x => this.getColour(x) + "0.6)")
        };

        const chartData = {
            data: {
                labels: dataTopics,
                datasets: [ownData, compareData]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            max: 100
                        }
                    }]
                }
            }
        };

        this.pChartData = chartData;
    }

    updateChartData(newChartData: { topics: Topic[], ownScores: Edge[], compareAgainst: Edge[] }) {
        this.calculateChartValues(newChartData);
    }

    @Watch("dataCategories")
    changedDataCategories(_oldTopics: Topic[], _newTopics: Topic[]) {
        this.$emit("changeTopics", this.dataCategories);
    }

    @Lifecycle
    mounted() {
        window.addEventListener("resize", this.updateChart);
        requestAnimationFrame(() => {
            this.updateChart();
        });
    }

    @Lifecycle
    created() {
        this.pDataGeneratorFunction = this.compareList();

        this.pExcludeTopics = this.dataCategories.filter(x => this.isDisabled(x)).map(x => x.id);
        // Register this.compareList with the event bus to ensure synchrocity with the rest of the app
        Fetcher.get(this.pDataGeneratorFunction as any,
            { compareTo: this.compare, excludeTopicIds: this.pExcludeTopics })
            .on(this.updateChartData);
        this.$emit("changeTopics", this.dataCategories);
    }

    @Lifecycle
    destroyed() {
        window.removeEventListener("resize", this.updateChart);
        Fetcher.get(this.pDataGeneratorFunction as any,
            { compareTo: this.compare, excludeTopicIds: this.pExcludeTopics })
            .off(this.updateChartData);
    }

    getColour(c: number) {
        if (c < 50) {
            return "rgba(255, 99, 132, ";
        } else if (c >= 50 && c <= 75) {
            return "rgba(255, 206, 86, ";
        } else {
            return "rgba(34, 85, 102, ";
        }
    };

    isDisabled(dataItem: Topic) {
        return !!this.hiddenData[dataItem.id];
    }

    getChartClass(chartValue: string) {
        return {
            "chartOption": true,
            "barChart": chartValue == "bar",
            "radarChart": chartValue == "radar",
            "topicDependency": chartValue == "topicDependency"
        };
    }

    get chartData() {
        if (this.pChartData !== undefined && this.pChartData.data !== undefined) {
            const ownData = this.pChartData.data.datasets[0];
            const compareData = this.pChartData.data.datasets[1];
            if (this.chart == "radar") {
                Object.assign(compareData, {
                    type: "radar",
                    pointStyle: "default",
                    backgroundColor: "rgba(0, 0, 0, 0.4)",
                    pointBorderColor: "rgba(0, 0, 0, 0.6)",
                    pointBackgroundColor: "rgba(0, 0, 0, 0.6)"
                });
                delete this.pChartData.options.scales;
                Object.assign(ownData, {
                    backgroundColor: ownData.backgroundColor[0],
                    borderColor: ownData.borderColor[0]
                });
            }
        }
        return this.pChartData;
    }

}
</script>
