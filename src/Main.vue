<template>
  <div id="main">
        <side-nav />
		<router-view />
  </div>
</template>

<style scoped>
</style>

<script lang="ts">
    import { Vue, Component } from "av-ts";
    import SideNav from "./components/SideNav";

    @Component({
        components: {
            SideNav
        }
    })
    export default class Main extends Vue {}
</script>
