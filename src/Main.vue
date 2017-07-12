<template>
    <md-layout>
        <md-layout md-flex="15">
            <side-nav></side-nav>
        </md-layout>
        <md-layout md-flex="80"
                   class="pageContent">
            <router-view></router-view>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .pageContent {
        min-width: 82.5%;
        -ms-flex: 0 1 82.5%;
        flex: 0 1 82.5%;
    }
</style>

<script lang="ts">
    import { Vue, Component } from "av-ts";
    import SideNav from "./components/SideNav.vue";

    @Component({
        components: {
            SideNav
        }
    })
    export default class Main extends Vue { }
</script>
