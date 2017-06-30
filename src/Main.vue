<template>
  <md-layout>
        <md-layout md-flex="15">
            <side-nav></side-nav>
        </md-layout>
        <md-layout md-flex="85">
    		<router-view></router-view>
        </md-layout>
  </md-layout>
</template>

<style scoped>
</style>

<script lang="ts">
    import { Vue, Component } from "av-ts";
    import SideNav from "./components/SideNav.vue";

    @Component({
        components: {
            SideNav
        }
    })
    export default class Main extends Vue {}
</script>
