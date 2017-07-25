<template>
    <md-layout>
        <md-layout class="sideNav">
            <side-nav></side-nav>
        </md-layout>
        <md-layout class="pageContent">
            <router-view></router-view>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .sideNav {
        min-width: 12.5%;
        flex: 0 1 12.5%;
    }
    
    .pageContent {
        margin-left: 1.25%;
        min-width: 85%;
        flex: 0 1 85%;
    }
</style>

<style>
    label {
        cursor: pointer;
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
