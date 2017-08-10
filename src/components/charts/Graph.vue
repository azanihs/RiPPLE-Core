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
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";

import * as d3 from "d3";

@Component()
export default class Graph extends Vue {
    width = 600;
    height = 300;

    edges = [];
    nodes = [];

    /*@Prop edges = p({
        type: Array,
        required: true
    });*/

    /*@Prop nodes = p({
        type: Array,
        required: true
    })*/

    @Lifecycle
    mounted() {
        this.nodes = TopicService.getAllAvailableTopics().map((x, i) => ({
            id: x,
            group: i
        }));

        this.nodes.forEach(x => {
            const randomNode = this.nodes[Math.floor(Math.random() * this.nodes.length)];
            //this.edges.push([x, randomNode, Math.random(), Math.random()]);
            this.edges.push({
                source: x,
                target: randomNode,
                weight: Math.random() * 10,
                colour: Math.random() * 10
            });
        });
        const minRange = 2;
        const maxRange = 10;
        const normalise = (min, max, v) => {
            return (maxRange - minRange) * ((v - min) / (max - min)) + minRange;
        };

        const nodeRadius = 20;
        const maxWeight = Math.max(...this.edges.map(x => x.weight));
        const minWeight = Math.min(...this.edges.map(x => x.weight));
        const lineColour = d3.interpolate("red", "#256");
        const maxColour = Math.max(...this.edges.map(x => x.colour));
        const minColour = Math.min(...this.edges.map(x => x.colour));
        const getStrokeColour = d => lineColour((d.colour - maxColour) / (minColour - maxColour));

        const svg = d3.select(this.$refs["svg"] as HTMLElement);

        const simulation = d3.forceSimulation(this.nodes)
            .alpha(2)
            .force("collision", d3.forceCollide(nodeRadius * 3).strength(1))
            .force("link", d3.forceLink(this.edges).distance(2 * nodeRadius).strength(0.8).distance(nodeRadius * 3))
            .force("body", d3.forceManyBody().theta(4))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2)) as any;

        const link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(this.edges)
            .enter()
            .append("line")
            .attr("stroke", getStrokeColour)
            .attr("stroke-width", d => normalise(minWeight, maxWeight, d.weight));

        const node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(this.nodes)
            .enter().append("circle")
            .attr("r", nodeRadius)
            .attr("stroke", "#444")
            .attr("fill", "#fff");

        const labels = svg.append("g")
            .attr("class", "labels")
            .selectAll("text")
            .data(this.nodes)
            .enter().append("text")
            .attr("dx", d => d.cx)
            .attr("dy", d => d.cy)
            .attr("text-anchor", "middle")
            .text(d => d.id);

        simulation
            .on("tick", this.ticked(link, node, labels, nodeRadius));
    }

    ticked(link, node, labels, radius) {
        return () => {
            node
                .attr("cx", d => {
                    d.x = Math.max(radius, Math.min(this.width - radius, d.x));
                    return d.x;
                })
                .attr("cy", d => {
                    d.y = Math.max(radius, Math.min(this.height - radius, d.y));
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
