<template>
    <div class="graphContainer">
        <graph v-for="(item, i) in data.datasets"
               :key="i"
               class="graph"
               :edges="item.data"
               :nodes="graphNodes"
               :shouldTick="i == 0"
               @graphElements="updateGraphQueue"
               @tick="ticked"
               @rescale="rescale"></graph>
    </div>
</template>

<style scoped>
.graphContainer {
    display: flex;
    flex: 1;
    height: 100%;
}

.graph:first-child {
    border-right: 1px solid #ccc;
}

.graph {
    width: 50%;
    height: 100%;
}
</style>

<script lang="ts">
import ChartJS from "chart.js";
import Graph from "./Graph.vue";
import { Vue, Component, Prop, Watch, Lifecycle, p } from "av-ts";

@Component({
    components: {
        Graph
    }
})
export default class GraphComparator extends Vue {
    @Prop
    data;

    @Prop
    nodes;

    chartQueue = [];

    get graphNodes() {
        return this.nodes;
    }

    clearQueue() {
        this.chartQueue = [];
    }

    updateGraphQueue(graph) {
        this.chartQueue.push(graph);
    }

    updateNodes() {
        this.chartQueue.forEach(x => {
            x.node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);

            x.link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            x.label
                .attr("dx", d => d.x)
                .attr("dy", d => d.y + 4);
        });
    }

    rescale(oldDimensions, newDimensions) {
        // Normalise data into new range
        const newX = nodeX => {
            return (nodeX / oldDimensions.width) * newDimensions.width;
        };
        const newY = nodeY => {
            return (nodeY / oldDimensions.height) * newDimensions.height;
        };
        this.chartQueue[0].node
            .attr("cx", d => {
                d.x = newX(d.x);
                return d.x;
            })
            .attr("cy", d => {
                d.y = newY(d.y);
                return d.y;
            });

        this.updateNodes();
    }

    ticked(graphWidth, graphHeight, radius) {
        if (this.chartQueue.length != this.data.datasets.length) {
            return setTimeout(() => {
                this.ticked(graphWidth, graphHeight, radius);
            }, 15);
        }
        this.chartQueue[0].node
            .attr("cx", d => {
                d.x = Math.max(radius, Math.min(graphWidth - radius, d.x));
            })
            .attr("cy", d => {
                d.y = Math.max(radius, Math.min(graphHeight - radius, d.y));
            });
        this.updateNodes();
    }
}
</script>
