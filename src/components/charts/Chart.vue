<template>
    <canvas v-if="type != 'topicDependency'"
            class="chartjs">
    </canvas>
    <div v-else-if="type == 'topicDependency'">
        <chart :edges="data.edges"
               :nodes="data.nodes"></chart>
        <chart :edges="data.edges"
               :nodes="data.nodes"></chart>
    </div>
</template>

<script lang="ts">
import ChartJS from "chart.js";
import Graph from "./Graph.vue";
import { Vue, Component, Prop, Watch, Lifecycle, p } from "av-ts";

@Component()
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
                destroy: () => { }
            };
        } else {
            const chartOptions = Object.assign({
                maintainAspectRatio: false,
                responsive: true
            }, this.options);

            this.chart = new ChartJS(this.$el, {
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

    @Watch("type")
    handleTypeChange() {
        this.resetChart();
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
</style>
