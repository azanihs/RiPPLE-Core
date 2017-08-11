<template>
    <div v-if="type != 'topicDependency'"
         class="chartContainer">
        <canvas class="chartjs"></canvas>
    </div>
    <div class="graphContainer"
         @resize="graphResize"
         v-else>
        <graph class="graph"
               ref="graph"
               :edges="data.datasets[0].data"
               :nodes="data.labels"></graph>
        <graph class="graph"
               ref="graph"
               :edges="data.datasets[1].data"
               :nodes="data.labels"></graph>
    </div>
</template>

<script lang="ts">
import ChartJS from "chart.js";
import Graph from "./Graph.vue";
import { Vue, Component, Prop, Watch, Lifecycle, p } from "av-ts";

@Component({
    components: {
        Graph
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

    graphResize = () => {
        this.chart.update();
    }

    mountChart() {
        if (this.type == "topicDependency") {
            this.chart = {
                destroy: () => { },
                update: () => {
                    this.$nextTick(() => {
                    });
                }
            };
        } else {
            const chartOptions = Object.assign({
                maintainAspectRatio: false,
                responsive: true
            }, this.options);

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

<style scoped>
.chartjs {
    max-width: 100%;
    margin: auto;
    transition: width 250ms linear, height 250ms linear;
}

.chartContainer {
    width: 100%;
    height: 100%;
}

.graphContainer {
    display: flex;
    flex: 1;
    height: 100%;
}

.graph {
    width: 50%;
    height: 100%;
}
</style>
