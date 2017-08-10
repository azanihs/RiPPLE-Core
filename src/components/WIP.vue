<template>
    <div>
        <h1>
            Work In Progress</h1>
        <graph></graph>
    </div>
</template>

<script lang="ts">
import { Vue, Component } from "av-ts";
import Graph from "./charts/Graph.vue";

@Component({
    components: {
        Graph
    }
})
export default class WIP extends Vue {

}
</script>
