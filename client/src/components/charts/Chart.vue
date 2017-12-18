<template>
    <div class="container">
        <div class="legend"
             v-if="type == 'bar' && data && data.datasets">
            <div class="legendItem">
                <span class="legendLabel rect"></span>
                <span>{{data.datasets[0].label}}</span>
            </div>
            <div class="legendItem">
                <span class="legendLabel">◯</span>
                <span>{{data.datasets[1].label}}</span>
            </div>
        </div>
        <div v-else-if="type == 'topicDependency'"
             class="graphLegend">
            <div class="legendItem ownLine">
                <span>IEdge Thickness is Number of Attempts</span>
            </div>
            <div class="legendItem">
                <span class="legendLabel rect"
                      style="background-color: pink"></span>
                <span>Low Competency</span>
            </div>
            <div class="legendItem">
                <span class="legendLabel rect"
                      style="background-color: #256"></span>
                <span>High Competency</span>
            </div>
        </div>

        <canvas v-if="type != 'topicDependency'"class="chartjs"></canvas>
        <graph-comparator v-else
                          :data="data"
                          :nodes="data.labels"></graph-comparator>
    </div>
</template>

<style scoped>
.graphContainer {
    display: flex;
    flex: 1;
    height: 100%;
}

.chartjs {
    max-width: 100%;
    margin: auto;
    transition: width 250ms linear, height 250ms linear;
}

.container {
    position: absolute;
    left: 0px;
    top: 0px;
    width: 100%;
    height: 100%;
}

.legend,
.graphLegend {
    flex: 1;
    display: flex;
    justify-content: center;
    flex-direction: row;
    flex-wrap: wrap;
}

.rect {
    height: 12px;
    width: 36px;
    display: inline-flex;
    background-color: #aaa;
}

.legendItem {
    margin: 0px 10px;
}

.ownLine {
    flex: 0 1 100%;
    text-align: center;
}

.legendLabel {
    color: #999;
}
</style>

<script lang="ts">
import ChartJS from "chart.js";
import GraphComparator from "./GraphComparator.vue";
import { Vue, Component, Prop, Watch, Lifecycle, p } from "av-ts";

@Component({
    components: {
        GraphComparator
    }
})
export default class ChartWrapper extends Vue {
    @Prop type = p<string>({
        required: true
    });

    @Prop data = p<Chart.ChartData>({
        required: true
    });

    @Prop options = p<Chart.ChartOptions>({
        default: () => {
            return {};
        }
    });

    chart: Chart | null = null;

    mountChart() {
        if (this.type == "topicDependency") {
            this.chart = {
                destroy: () => { },
                update: () => { }
            } as Chart;
        } else {
            const chartOptions: Chart.ChartOptions = Object.assign({
                maintainAspectRatio: false,
                responsive: true
            }, this.options);

            if (this.type === "bar") {
                if (chartOptions.legend === undefined) {
                    chartOptions.legend = {};
                }
                chartOptions.scales = {
                    yAxes: [{
                        ticks: {
                            max: 100
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            autoSkip: false
                        }
                    }]
                };
                chartOptions.legend.display = false;
            } else if (this.type == "radar") {
                chartOptions.scales = {
                    ticks: {
                        display: false
                    }
                };
            }
            const canvas = this.$el.querySelector("canvas")!;
            this.chart = new ChartJS(canvas.getContext("2d")!, {
                type: this.type,
                data: this.data,
                options: chartOptions
            });
            this.chart.resize();
        }
    }

    @Lifecycle
    mounted() {
        this.mountChart();
    }

    resetChart() {
        window.dispatchEvent(new Event("resize"));
        this.$nextTick(() => {
            this.chart!.destroy();
            this.mountChart();
        });
    }

    @Lifecycle
    beforeUpdate() {
        if (this.type == "topicDependency") {
            this.chart!.destroy();
        }
    }

    @Watch("type")
    handleTypeChange(_oldType: string, _newType: string) {
        if (this.type == "topicDependency") {
            this.chart!.destroy();
            this.$nextTick(() => {
                this.mountChart();
            });
        } else {
            this.resetChart();
        }
    }

    @Watch("options")
    handleOptionsChange(_oldOptions: Chart.ChartOptions, _newOptions: Chart.ChartOptions) {
        this.resetChart();
    }

    @Watch("data")
    handleDataChange(_oldData: Chart.ChartData, _newData: Chart.ChartData) {
        this.chart!.update();
    }
}
</script>


