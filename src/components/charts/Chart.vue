<template>
    <canvas class="chartjs" :width="width" :height="height">
    </canvas>
</template>

<script lang="ts">
import ChartJS from "chart.js";
import { Vue, Component, Prop, Watch, Lifecycle, p } from "av-ts";
const types = ["line", "bar", "radar", "polarArea", "pie", "doughnut", "bubble"];

@Component()
export default class Chart extends Vue {
    @Prop type = p({
        type: String,
        required: true
        //validator: val => types.find(val)
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

    get height() {
        if (this.$el) {
            return this.$el.parentElement.getBoundingClientRect().height;
        }
    }
    get width() {
        if (this.$el) {
            return this.$el.parentElement.getBoundingClientRect().width;
        }
    }

    mountChart() {
        const chartOptions = Object.assign({
            maintainAspectRatio: false,
            responsive: this.type == "radar" ? false : true
        }, this.options);

        this.chart = new ChartJS(this.$el, {
            type: this.type,
            data: this.data,
            options: chartOptions
        });
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
