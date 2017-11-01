<template>
    <svg xmlns="http://www.w3.org/2000/svg"
         xmlns:xlink="http://www.w3.org/1999/xlink"
         ref="svg"
         :width="width"
         :height="height">
    </svg>
</template>

<style scoped>
svg {}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Watch, Prop, p } from "av-ts";
import UserService from "../../services/UserService";

import * as d3 from "d3";

@Component()
export default class Graph extends Vue {

    willAnimateNextChange = true;
    simulationIsFinished = false;

    graphWidth = 0;
    graphHeight = 0

    nodeRadius = 20;

    width = 0;
    height = 0;
    @Prop edges = p({
        type: Array,
        required: true
    });

    @Prop nodes = p({
        type: Array,
        required: true
    });
    @Prop
    shouldTick: boolean;

    simulation = null;

    render() {
        const edges = this.edges.slice();
        const nodes = this.nodes.slice();

        const selfLoops = edges.filter(x => x.source == x.target);

        const minRange = 2;
        const maxRange = 10;
        const normalise = (min, max, v) => {
            return (maxRange - minRange) * ((v - min) / (max - min)) + minRange;
        };

        const nodeRadius = this.nodeRadius;
        const maxWeight = Math.max(...edges.map(x => x.attempts));
        const minWeight = Math.min(...edges.map(x => x.attempts));
        const lineColour = d3.interpolate("pink", "#256");
        const maxColour = Math.max(...edges.map(x => x.competency));
        const minColour = Math.min(...edges.map(x => x.competency));
        const getStrokeColour = d => lineColour((d.competency - maxColour) / (minColour - maxColour));

        const svg = d3.select(this.$refs["svg"] as HTMLElement);
        svg.html(null);

        const container = svg
            .append("g")
            .attr("class", "container")
            .attr("transform", `translate(${nodeRadius},${nodeRadius})`);

        this.graphWidth = this.width - (nodeRadius * 2);
        this.graphHeight = this.height - (nodeRadius * 2);

        const forceLink = d3.forceLink(edges);

        this.simulation = d3.forceSimulation(nodes)
            .alpha(3)
            .force("collision", d3.forceCollide(3 * nodeRadius))
            .force("link", forceLink.distance(3 * nodeRadius))
            .force("body", d3.forceManyBody().distanceMin(nodeRadius))
            .force("center", d3.forceCenter(this.graphWidth / 2, this.graphHeight / 2)) as any;

        const link = container.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(edges)
            .enter()
            .append("line")
            .attr("stroke", getStrokeColour)
            .attr("stroke-width", d => normalise(minWeight, maxWeight, d.attempts));

        const node = container.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", nodeRadius)
            .attr("stroke", d => {
                const foundSelfLoop = selfLoops.find(selfLoop => selfLoop.source == d);
                if (foundSelfLoop) {
                    return getStrokeColour(foundSelfLoop);
                }
                return "#444";
            })
            .attr("stroke-width", d => {
                const foundSelfLoop = selfLoops.find(selfLoop => selfLoop.source == d);
                if (foundSelfLoop) {
                    return normalise(minWeight, maxWeight, foundSelfLoop.attempts);
                }
                return 1;
            })
            .attr("fill", "#fff");

        const label = container.append("g")
            .attr("class", "labels")
            .selectAll("text")
            .data(nodes)
            .enter().append("text")
            .attr("dx", d => d.cx)
            .attr("dy", d => d.cy)
            .attr("text-anchor", "middle")
            .text(d => d.id);

        this.$emit("graphElements", {
            node: node,
            link: link,
            label: label
        });

        this.simulation.on("end", () => {
            this.simulationIsFinished = true;
        });

        if (this.shouldTick) {
            if (this.willAnimateNextChange) {
                this.simulation
                    .on("tick", this.ticked(nodeRadius * 2));
            } else {
                this.computeStaticLayout();
            }
        } else {
            this.simulation.stop();
        }
    }

    @Watch("edges")
    edgeChange() {
        this.render();
    }

    @Watch("nodes")
    nodeChange() {
        this.render();
    }

    updateDimensions() {
        const { width, height } = this.$el.getBoundingClientRect();
        if (!this.simulationIsFinished) {
            this.computeStaticLayout();
            return;
        }
        const oldWidth = this.width;
        const oldHeight = this.height;
        this.width = width;
        this.height = height;
        this.$emit("rescale",
            { width: oldWidth, height: oldHeight },
            { width: width, height: height }
        );
    }

    @Lifecycle
    mounted() {
        if (this.shouldTick) {
            window.addEventListener("resize", this.updateDimensions);
        }
        const { width, height } = this.$el.getBoundingClientRect();
        this.width = width;
        this.height = height;
        this.render();
    }

    @Lifecycle
    destroyed() {
        if (this.shouldTick) {
            window.removeEventListener("resize", this.updateDimensions);
        }
    }

    ticked(radius) {
        return () => {
            this.willAnimateNextChange = false;
            this.$emit("tick", this.graphWidth, this.graphHeight, radius);
        };
    }

    computeStaticLayout() {
        this.simulation.stop();
        this.simulation.on("tick", null);

        const end = Math.ceil(Math.log(this.simulation.alphaMin()) / Math.log(1 - this.simulation.alphaDecay()));
        for (let i = 0; i < end; i++) {
            this.simulation.tick();
        }

        this.ticked(this.nodeRadius * 2)();
        this.simulationIsFinished = true;
    }
}
</script>
