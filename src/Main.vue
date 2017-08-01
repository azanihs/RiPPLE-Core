<template>
    <md-layout>
        <md-layout md-hide-xsmall md-hide-small md-hide-medium class="sideNavContainer">
            <side-nav class="sideNav"></side-nav>
        </md-layout>
        <md-layout md-hide-xsmall md-hide-small md-hide-medium class="pageContent">
            <router-view></router-view>
        </md-layout>
    
        <md-layout md-hide-large-and-up class="mobileSideNavContainer">
            <side-nav class="sideNav"></side-nav>
        </md-layout>
        <md-layout md-hide-large-and-up class="mobilePageContent">
            <router-view></router-view>
        </md-layout>
    </md-layout>
</template>

<style scoped>
.sideNavContainer {
    min-width: 12.5%;
    flex: 0 1 12.5%;
}

.pageContent {
    margin-left: 1.25%;
    min-width: 85%;
    flex: 0 1 85%;
}

.mobileSideNavContainer {
    min-width: 52px;
    flex: 0 1 52px;
    position: relative;
}

.mobileSideNavContainer .sideNav {
    width: 100%;
}

.sideNav {
    position: absolute;
    height: 100%;
    width: 12.5%;
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
