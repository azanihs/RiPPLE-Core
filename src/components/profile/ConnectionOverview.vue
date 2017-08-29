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
import { Vue, Component } from "av-ts";

import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";

@Component()
export default class ConnectionOverview extends Vue {

    pTopics = [];
    pPeers = [];

    get peerConnections() {
        UserService.getUserPeers(newPeers => {
            this.pPeers = newPeers;
        });

        return this.pPeers;
    }

    get profileData() {
        return UserService.getLoggedInUser();
    }

    get topics() {
        TopicService.getAllAvailableTopics(newTopics => {
            this.pTopics = newTopics;
        });

        return this.pTopics;
    }

    get categories() {
        return UserService.getAllAvailableCategories();
    }
}
</script>
