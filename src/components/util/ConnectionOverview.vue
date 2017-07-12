<template>
    <md-layout>
        <h2>Connection Overview</h2>
        <connectedness-heatmap :data="profileData"
                               :topics="topics"
                               :categories="categories">
        </connectedness-heatmap>
        <h2>Peer Connections</h2>
        <md-layout md-flex="100">
            <md-image v-for="peer in peerConnections"
                      :key="peer.id"
                      class="connectionImage"
                      :md-src="peer.image"></md-image>
        </md-layout>
    </md-layout>
</template>
<style scoped>
    h2 {
        width: 100%;
        padding-top: 0.75em;
    }
    
    .connectionImage {
        width: 50px;
        height: 50px;
        margin: 6px;
        border: 2px solid #ccc;
        cursor: pointer;
        transition: opacity 1.1s cubic-bezier(.25, .8, .25, 1), filter 2.2s cubic-bezier(.25, .8, .25, 1) .3s, border 500ms ease !important;
    }
    
    .connectionImage:hover {
        border-color: #256;
    }
</style>

<script lang="ts">
    import { Vue, Component, Prop } from "av-ts";
    import Chart from "../charts/Chart.vue";
    import ConnectednessHeatmap from "./ConnectednessHeatmap.vue";
    import UserRepository from "../../repositories/UserRepository";
    import UserService from "../../services/UserService";

    @Component({
        components: {
            "connectedness-heatmap": ConnectednessHeatmap
        }
    })
    export default class ConnectionOverview extends Vue {

        get peerConnections() {
            return UserService.getUserPeers();
        }

        get profileData() {
            return UserRepository.getLoggedInUser();
        }
        get topics() {
            return UserRepository.getAllAvailableTopics();
        }

        get categories() {
            return UserRepository.getAllAvailableCategories();
        }
    }
</script>
