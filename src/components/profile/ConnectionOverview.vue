<template>
    <md-card>
        <md-layout>
            <h2>Peer Connections</h2>
            <md-layout md-flex="100">
                <md-image v-for="peer in peerConnections"
                          :key="peer.id"
                          class="connectionImage"
                          :md-src="peer.image"></md-image>
            </md-layout>
        </md-layout>
    </md-card>
</template>
<style scoped>
h2 {
    width: 100%;
    margin-top: 0px;
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
import { Vue, Component, Lifecycle } from "av-ts";

import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";
import Fetcher from "../../services/Fetcher";

@Component()
export default class ConnectionOverview extends Vue {

    pPeers = [];
    updatePeers(newPeers) {
        this.pPeers = newPeers;
    };

    @Lifecycle
    created() {
        Fetcher.get(UserService.getUserPeers, { count: 50 })
            .on(this.updatePeers);
    }
    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getUserPeers)
            .off(this.updatePeers);
    }

    get peerConnections() {
        return this.pPeers;
    }
}
</script>
