<template>
    <div class="chartContainer">
        <div class="legend"
             v-if="type == 'bar' && data && data.datasets">
            <div class="legendItem">
                <span class="legendLabel rect"></span>
                <span>{{data.datasets[0].label}}</span>
            </div>
            <div class="legendItem">
                <span class="legendLabel">▲</span>
                <span>{{data.datasets[1].label}}</span>
            </div>
        </div>
        <div v-else-if="type == 'topicDependency'"
             class="graphLegend">
            <div class="legendItem ownLine">
                <span>Edge Thickness is Number of Attempts</span>
            </div>
            <div class="legendItem">
                <span class="legendLabel rect"
                      style="background-color: pink"></span>
                <span>Poor Competency</span>
            </div>
            <div class="legendItem">
                <span class="legendLabel rect"
                      style="background-color: #256"></span>
                <span>Superior Competency</span>
            </div>
        </div>

        <div v-if="type != 'topicDependency'"
             class="chartContainer">
            <canvas class="chartjs"></canvas>
        </div>
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

.chartContainer {
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
export default class Chart extends Vue {
    @Prop type = p({
        type: String,
        required: true
    });
    @Prop data = p({
        type: Object,
        required: true,
        default: () => {
            return {};
        }
    });

    @Prop options = p({
        type: Object,
        default: () => {
            return {};
        }
    });

    chart: ChartJS = null;

    mountChart() {
        if (this.type == "topicDependency") {
            this.chart = {
                destroy: () => { },
                update: () => { }
            };
        } else {
            const chartOptions = Object.assign({
                maintainAspectRatio: false,
                responsive: true
            }, this.options);

            if (this.type === "bar") {
                if (chartOptions["legend"] === undefined) {
                    chartOptions["legend"] = {};
                }
                chartOptions["legend"].display = false;
            }

            this.chart = new ChartJS(this.$el.querySelector("canvas"), {
                type: this.type,
                data: this.data,
                options: chartOptions
            });
        }
    }

    @Lifecycle
    mounted() {
        this.mountChart();
        setTimeout(() => {
            this.resetChart();
        }, 10);
    }

    resetChart() {
        this.$nextTick(() => {
            this.chart.destroy();
            this.mountChart();
        });
    }

    @Lifecycle
    beforeUpdate() {
        if (this.type == "topicDependency") {
            this.chart.destroy();
        }
    }

    @Watch("type")
    handleTypeChange() {
        if (this.type == "topicDependency") {
            this.chart.destroy();
            this.$nextTick(() => {
                this.mountChart();
            });
        } else {
            this.resetChart();
        }
    }

    @Watch("options")
    handleOptionsChange() {
        this.resetChart();
    }

    @Watch("data")
    handleDataChange() {
        this.chart.update();
    }
}
</script>


