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
    width = 600;
    height = 300;

    graphWidth = 0;
    graphHeight = 0

    @Prop edges = p({
        type: Array,
        required: true
    });

    @Prop nodes = p({
        type: Array,
        required: true
    });

    formattedEdges = [];
    formattedNodes = [];

    render() {
        this.formattedEdges = this.edges.map(x => ({
            source: x[0],
            target: x[1],
            weight: x[2],
            colour: x[3]
        }));
        this.formattedNodes = this.nodes;
        const selfLoops = this.formattedEdges.filter(x => x.source == x.target);

        const minRange = 2;
        const maxRange = 10;
        const normalise = (min, max, v) => {
            return (maxRange - minRange) * ((v - min) / (max - min)) + minRange;
        };

        const nodeRadius = 20;
        const maxWeight = Math.max(...this.formattedEdges.map(x => x.weight));
        const minWeight = Math.min(...this.formattedEdges.map(x => x.weight));
        const lineColour = d3.interpolate("pink", "#256");
        const maxColour = Math.max(...this.formattedEdges.map(x => x.colour));
        const minColour = Math.min(...this.formattedEdges.map(x => x.colour));
        const getStrokeColour = d => lineColour((d.colour - maxColour) / (minColour - maxColour));

        const svg = d3.select(this.$refs["svg"] as HTMLElement);
        svg.html(null);

        const container = svg
            .append("g")
            .attr("class", "container")
            .attr("transform", `translate(${nodeRadius},${nodeRadius})`);

        this.graphWidth = this.width - (nodeRadius * 2);
        this.graphHeight = this.height - (nodeRadius * 2);


        const forceLink = d3.forceLink(this.formattedEdges);
        const simulation = d3.forceSimulation(this.formattedNodes)
            .alpha(3)
            .force("collision", d3.forceCollide(3 * nodeRadius).strength(1))
            .force("link", forceLink.distance(3 * nodeRadius).strength(0.8))
            .force("body", d3.forceManyBody().distanceMin(nodeRadius))
            .force("center", d3.forceCenter(this.graphWidth / 2, this.graphHeight / 2)) as any;

        const link = container.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(this.formattedEdges)
            .enter()
            .append("line")
            .attr("stroke", getStrokeColour)
            .attr("stroke-width", d => normalise(minWeight, maxWeight, d.weight));

        const node = container.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(this.formattedNodes)
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
                    return normalise(minWeight, maxWeight, foundSelfLoop.weight);
                }
                return 1;
            })
            .attr("fill", "#fff");

        const labels = container.append("g")
            .attr("class", "labels")
            .selectAll("text")
            .data(this.formattedNodes)
            .enter().append("text")
            .attr("dx", d => d.cx)
            .attr("dy", d => d.cy)
            .attr("text-anchor", "middle")
            .text(d => d.id);

        simulation
            .on("tick", this.ticked(link, node, labels, nodeRadius));
    }

    @Watch("edges")
    edgeChange() {
        this.render();
    }

    @Watch("nodes")
    nodeChange() {
        this.render();
    }

    @Lifecycle
    mounted() {
        this.render();
    }

    ticked(link, node, labels, radius) {
        return () => {
            node
                .attr("cx", d => {
                    d.x = Math.max(radius, Math.min(this.graphWidth - radius, d.x));
                    return d.x;
                })
                .attr("cy", d => {
                    d.y = Math.max(radius, Math.min(this.graphHeight - radius, d.y));
                    return d.y;
                });

            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            const data = node.data();
            labels
                .attr("dx", (d, i) => data[i].x)
                .attr("dy", (d, i) => data[i].y + 4);
        };
    }
}
</script>
