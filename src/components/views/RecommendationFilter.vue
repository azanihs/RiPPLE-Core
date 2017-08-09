<template>
    <md-card class="fullWidth">
        <md-layout md-flex="100">
            <md-layout md-flex="65"
                       class="leftPanel">
                <h2 class="chartHeader">Your Current Competencies</h2>
                <div class="chartContainer">
                    <div class="chartPanel">
                        <chart :type="'bar'"
                               :data="chartData.data"
                               :options="chartData.options"></chart>
                    </div>
                </div>
            </md-layout>
            <md-layout md-flex="35"
                       class="rightPanel">
                <div class="settingsContainer">
                    <div class="visualisationMenu">
                        <slot></slot>
                    </div>
                </div>
            </md-layout>
        </md-layout>
    </md-card>
</template>
<style scoped>
.fullWidth {
    width: 100%;
    user-select: none;
    padding: 0px !important;
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

.settingsContainer {
    margin: 0px auto auto auto;
}

.visualisationMenu>h3 {
    margin-top: 0px;
}
</style>

        <script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import UserService from "../../services/UserService";
import Chart from "../charts/Chart.vue";

@Component({
    components: {
        Chart
    }
})
export default class RecommendationFilter extends Vue {
    @Prop
    topics = p({
        required: true,
        type: Array
    }) as string[];

    hiddenData = {};
    getColour(c) {
        if (c < 50) {
            return "rgba(255, 99, 132, ";
        } else if (c >= 50 && c <= 75) {
            return "rgba(255, 206, 86, ";
        } else {
            return "rgba(34, 85, 102, ";
        }
    };

    isDisabled(dataItem) {
        return !!this.hiddenData[dataItem];
    }

    toggleVisible(dataItem) {
        if (this.hiddenData[dataItem]) {
            this.$set(this.hiddenData, dataItem, false);
        } else {
            this.$set(this.hiddenData, dataItem, true);
        }

        const topicsToShow = this.topics.filter(x => !this.isDisabled(x));
        this.$emit("changeTopics", topicsToShow);
    }

    updateChart() {
        const dim = this.$el.querySelector(".visualisationMenu").getBoundingClientRect();
        this.$el.querySelector(".chartContainer")["style"].height = dim.height + "px";
    }

    @Lifecycle
    created() {
        this.$emit("changeTopics", this.topics);
    }

    @Lifecycle
    mounted() {
        window.addEventListener("resize", this.updateChart);
        this.$nextTick()
            .then(this.updateChart);
    }

    @Lifecycle
    destroyed() {
        window.removeEventListener("resize", this.updateChart);
    }

    get chartData() {
        const items = this.topics.filter(x => !this.isDisabled(x));
        const { topics, ownScore } = UserService.userCompetencies(items);

        const ownData = {
            data: ownScore,
            label: "Your Competencies",
            backgroundColor: ownScore.map(x => this.getColour(x) + "0.4)"),
            borderColor: ownScore.map(x => this.getColour(x) + "1)"),
            borderWidth: 2
        };

        return {
            data: {
                labels: topics,
                datasets: [ownData]
            },
            options: {
                legend: {
                    display: false
                },
                scale: {
                    ticks: {
                        beginAtZero: true
                    }
                }
            }
        };
    }
}
</script>
