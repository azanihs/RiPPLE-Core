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
        const dim = this.$el.parentElement.getBoundingClientRect();
        // Need to test cross-browser implications of disabling this
        // this.$el.setAttribute("width", "" + dim.width);
        // this.$el.setAttribute("height", "" + dim.height);
        this.$el.style.width = "100%";
        this.$el.style.height = "100%";

        setTimeout(() => {
            this.resetChart();
        }, 10);
    }

    resetChart() {
        this.$nextTick(() => {
            if (this.chart) {
                this.chart.destroy();
            }

            this.chart = new ChartJS(this.$el, {
                type: this.type,
                data: this.data,
                options: this.options,
                responsive: true
            });
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
}
</style>
