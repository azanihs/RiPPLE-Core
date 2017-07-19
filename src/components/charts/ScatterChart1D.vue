<template>
    <div class="chart">
        <md-chip class="tooltip"
                 v-bind:class="tooltip.class"
                 v-bind:style="tooltip.style">{{ tooltip.text }}</md-chip>
        <svg xmlns="http://www.w3.org/2000/svg"
             v-bind:style="{width: viewPort.width+'px', height: viewPort.height+'px'}">
            <g class="axis">
                <g class="axisLines">
                    <line v-for="x in calculatedData.axis"
                          :key="x"
                          :x1="x.x1"
                          :x2="x.x2"
                          :y1="x.y1"
                          :y2="x.y2"></line>
                </g>
                <g class="axisLabels">
                    <text v-for="x in calculatedData.axisLabels"
                          :key="x"
                          :dy="x.dy"
                          :dx="x.dx"
                          :y="x.y"
                          :x="x.x"
                          text-anchor="middle">{{x.text}}</text>
                </g>
                <g class="axisGrid">
                    <line v-for="x in calculatedData.grid"
                          :key="x"
                          :x1="x.x1"
                          :x2="x.x2"
                          :y1="x.y1"
                          :y2="x.y2"></line>
                </g>
                <g class="gridLabels">
                    <text v-for="x in calculatedData.gridLabels"
                          :key="x"
                          :dy="x.dy"
                          :dx="x.dx"
                          :y="x.y"
                          :x="x.x"
                          text-anchor="middle">{{x.text}}</text>
                </g>
            </g>
            <g class="points">
                <circle v-for="x in calculatedData.scatter"
                        v-bind:class="{ selected: propSelectedNodes[x.original.id], hidden: propHiddenNodes[x.original.id], centroid: x.type == 'centroid' }"
                        :key="x.original.id"
                        :cx="x.cx"
                        :cy="x.cy"
                        :fill="x.fill"
                        :r="x.r"
                        @click="circleClick($event, x)"
                        @mousemove="circleHover($event, x)"
                        @mouseout="circleLeave($event, x)" />
            </g>
        </svg>
    </div>
</template>

<style scoped>
    .chart {
        transform: translate3d(0, 0, 0);
        width: 100%;
        height: 100%;
    }
    
    svg,
    .tooltip {
        user-select: none;
    }
    
    svg .axisLines line,
    svg .axisGrid line {
        stroke: #333;
        stroke-width: 1px;
        opacity: 0.15;
    }
    
    svg .points circle:hover {
        stroke-width: 2px !important;
    }
    
    svg circle {
        stroke: #000;
        stroke-width: 0.25px;
        opacity: 1;
    }
    
    svg circle.selected {
        opacity: 1 !important;
        stroke-width: 0.5px;
    }
    
    svg circle.centroid.hidden {
        stroke: 0.5px;
        opacity: 1;
    }
    
    .tooltip {
        z-index: 1000;
        position: fixed;
    
        color: #fff;
        pointer-events: none;
        opacity: 0;
    }
    
    .tooltipVisible {
        opacity: 0.75
    }
    
    .md-theme-default.md-chip {
        background-color: #333;
    }
</style>


<script lang="ts">
    import { Vue, Component, Prop, Lifecycle, p } from "av-ts";
    import {
        ScatterPoint, ChartConfiguration, DisplaySettings, Circle, DataContainer
    } from "../../interfaces/chart";
    import * as d3 from "d3";

    @Component()
    export default class ScatterChart1D extends Vue {
        @Prop propData;
        @Prop propSelectedNodes = p({
            type: Object,
            default: () => ({})
        });

        @Prop propHiddenNodes = p({
            type: Object,
            default: () => ({})
        });

        tooltipTimeout = -1;
        tooltip = {
            style: {
                left: "0px",
                top: "0px"
            },
            class: {
                tooltipVisible: false
            },
            text: ""
        };

        calculatedData = {
            scatter: [],
            axis: [],
            axisLabels: [],
            grid: [],
            gridLabels: []
        };

        // The input data to transform
        private chartData: ScatterPoint[];

        // Chart configuration and screen setting sizes.
        private chartConfiguration: ChartConfiguration;

        // By default screen size is the same as parent container
        private viewPort = {
            width: 0,
            height: 0,
            radius: 0,
            xView: 0,
            yView: 0
        };

        // Minimum and maximum values of the dataset. Used to calculate axis ranges
        private minV = { x: 0 };
        private maxV = { x: 0 };

        @Lifecycle
        created() {
            this.chartData = JSON.parse(JSON.stringify(this.propData));

            let xVals: number[] = this.chartData.map(x => x.value);
            this.minV.x = d3.min(xVals);
            this.maxV.x = d3.max(xVals);
        }

        @Lifecycle
        mounted() {
            this.updateDimensions();
            this.redraw();

            window.addEventListener("resize", () => {
                this.updateDimensions();
                this.redraw();
            });
        }

        /**
        * Sets the chart dimensions such as width and height
        */
        setDimensions(settings: DisplaySettings): ScatterChart1D {
            this.viewPort = Object.assign({}, this.viewPort, settings);
            return this;
        };

        /**
        * Returns an object which has vectors that define the chart axis
        */
        private generateAxisDimensions() {
            let xView = this.viewPort.xView;
            let yView = this.viewPort.yView;
            let height = this.viewPort.height;
            let width = this.viewPort.width;
            return [{ // Y
                type: "y",
                view: this.viewPort.yView,
                intersect: {
                    x: [-(this.viewPort.width - xView) / 2, (width - xView) / 2]
                },
                x0: -(width - xView) / 2, x1: -(width - xView) / 2
            }];
        }

        /**
        *  Generates the chart axis data (such as the ticks, grid, and axis labels)
        */
        private getAxisData(dimensions, normalise): DataContainer {
            return dimensions.reduce((carry: DataContainer, point) => {
                // Push axis label
                carry.axisLabels.push({
                    dx: this.viewPort.width / 2,
                    dy: this.viewPort.height - 10,
                    y: 0, x: 0,
                    text: ""
                });
                carry.axis.push({
                    x1: this.viewPort.width / 2,
                    x2: this.viewPort.width / 2,
                    y1: 10,
                    y2: this.viewPort.height - 10
                });

                const scale = d3.scaleLinear()
                    .domain([0, 100])
                    .range([this.viewPort.height - 10, 10]);
                const axisValues = scale.ticks();

                axisValues.forEach((tickValue, i) => {
                    let yPos = scale(tickValue);
                    carry.gridLabels.push({ // Tick Labels
                        dx: this.viewPort.width / 2 - 20,
                        dy: yPos + 6,
                        y: 0, x: 0,
                        text: "" + tickValue
                    });

                    carry.grid.push({ // Grid Lines
                        x1: this.viewPort.width / 2 - 5,
                        x2: this.viewPort.width / 2 + 20,
                        y1: yPos,
                        y2: yPos
                    });
                });
                return carry;
            }, { axis: [], axisLabels: [], grid: [], gridLabels: [] });
        }

        /**
        *  Calculates the position of each scatter point, and also generates the axis information
        */
        private calculatePositions(): void {
            let normalise = (value, axis, range): number => {
                let numerator = value - this.minV[axis];
                let denominator = this.maxV[axis] - this.minV[axis];
                return (numerator / denominator) * range - (range / 2);
            };

            let scale = d3.scaleLinear()
                .domain([0, 100])
                .range([this.viewPort.height - 10, 10]);

            let mapScatterPoints: (point: ScatterPoint) => Circle = point => {
                // Normalise points in range of min/max
                let xTrans = this.viewPort.width / 2;
                let yTrans = scale(point.value);
                return {
                    transform: `translate(${xTrans}, ${yTrans})`,
                    cx: xTrans,
                    cy: yTrans,
                    fill: point.fill,
                    original: point,
                    r: 2.5
                };
            };

            if (this.calculatedData.scatter.length != this.chartData.length) {
                this.calculatedData.scatter = this.chartData.map(mapScatterPoints);
            } else {
                this.chartData.forEach((scatter, i) => {
                    const updated = mapScatterPoints(scatter);
                    this.calculatedData.scatter[i].cx = updated.cx;
                    this.calculatedData.scatter[i].cy = updated.cy;
                });
            }

            let axisData = this.getAxisData(this.generateAxisDimensions(),
                normalise);

            this.calculatedData.axis = axisData.axis;
            this.calculatedData.axisLabels = axisData.axisLabels;
            this.calculatedData.grid = axisData.grid;
            this.calculatedData.gridLabels = axisData.gridLabels;
        };

        circleClick = (e: MouseEvent, node: Circle) => {
            this.$emit("circleClick", e, node);
        }
        circleHover = (e: MouseEvent, node: Circle) => {
            if (this.tooltipTimeout != -1) {
                clearTimeout(this.tooltipTimeout);
            }
            this.tooltip.style.left = (node.cx + 10) + "px";
            this.tooltip.style.top = (node.cy) + "px";
            this.tooltip.class.tooltipVisible = true;
            this.tooltip.text = `${node.original.value}`;
            this.$emit("circleHover", e, node);
        }

        circleLeave = (e: MouseEvent, node: Circle) => {
            if (this.tooltipTimeout != -1) {
                clearTimeout(this.tooltipTimeout);
            }

            this.tooltipTimeout = setTimeout(() => {
                this.tooltip.class.tooltipVisible = false;
            }, 100);
            this.$emit("circleLeave", node);
        }

        updateDimensions(): boolean {
            let bBox = this.$el.parentElement.getBoundingClientRect();

            if (bBox.width == this.viewPort.width &&
                bBox.height == this.viewPort.height) {
                return false;
            }

            this.setDimensions({
                width: bBox.width,
                height: bBox.height,
                depth: (bBox.width + bBox.height) / 2,
                xView: bBox.width / 2,
                yView: bBox.height / 2,
                zView: (bBox.width + bBox.height) / 4,
                radius: Math.min(bBox.width / 2, bBox.height / 2)
            });
            return true;
        }

        /**
        * Re-calcualtes data positions and draws them on the DOM
        */
        redraw(): ScatterChart1D {
            this.calculatePositions();

            return this;
        };
    }
</script>
