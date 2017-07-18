<template>
    <svg xlms="http //www.w3.org/2000/svg">
        <rect></rect>
        <line></line>
    </svg>
</template>

<style scoped>
    
</style>


<script lang="ts">
    import { Vue, Component, Prop, Lifecycle } from "av-ts";

    @Component()
    export default class BulletChart extends Vue {
        @Prop data;

        @Lifecycle
        mounted() {

        }
    }
</script>
