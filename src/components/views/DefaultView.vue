<template>
    <connectedness-heatmap />
</template>

<style scoped>
    
</style>

<script lang="ts">
    import { Vue, Component } from "av-ts";
    import ConnectednessHeatmap from "../util/ConnectednessHeatmap.vue";

    @Component({
        components: {
            "connectedness-heatmap": ConnectednessHeatmap
        }
    })
    export default class DefaultView extends Vue { }
</script>
