<template>
    <div>
        <h1>
            Work In Progress</h1>
        <graph :nodes="nodes"
            :edges="edges"></graph>
        <graph :nodes="nodes"
            :edges="otherEdges"></graph>
    </div>
</template>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import TopicService from "../services/TopicService";

import Graph from "./charts/Graph.vue";

@Component({
    components: {
        Graph
    }
})
export default class WIP extends Vue {
    get nodes() {
        return TopicService.getAllAvailableTopics().map((x, i) => ({
            id: x
        }));
    }

    get edges() {
        return this.nodes.map(x => {
            const randomNode = this.nodes[Math.floor(Math.random() * this.nodes.length)];
            return [x, randomNode, Math.random(), Math.random()];
        });
    }
    get otherEdges() {
        return this.nodes.map(x => {
            const randomNode = this.nodes[Math.floor(Math.random() * this.nodes.length)];
            return [x, randomNode, Math.random(), Math.random()];
        });
    }
}
</script>
