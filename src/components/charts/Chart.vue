<template>
    <canvas class="chartjs">
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

    @Lifecycle
    mounted() {
        this.chart = new ChartJS(this.$el, {
            type: this.type,
            data: this.data,
            options: Object.assign({
                maintainAspectRatio: false
            }, this.options)
        });

        setTimeout(() => {
            this.resetChart();
        }, 10);
    }

    resetChart() {
        this.$nextTick(() => {
            setTimeout(() => {
                this.chart.destroy();
                this.chart = new ChartJS(this.$el, {
                    type: this.type,
                    data: this.data,
                    options: Object.assign({
                        maintainAspectRatio: false
                    }, this.options)
                });
            }, 50);
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
}
</style>
