<template>
    <md-layout md-flex="95">
        <md-layout md-flex="100" class="headingContainer">
            <h1>Connect With Peers</h1>
            <availability-selector />
        </md-layout>
        <md-layout class="headingContainer">
            <h1>Review Recommendations</h1>
        </md-layout>
        <md-layout class="fullHeight" md-flex="100">
            <md-tabs md-fixed class="md-transparent">
                <md-tab md-label="BE A MENTOR">
                    <recommendations :peers="peersToMentor" />
                </md-tab>
                <md-tab md-label="NEED A MENTOR">
                    <recommendations :peers="peersToBeMentored" />
                </md-tab>
                <md-tab md-label="STUDY WITH PEER">
                    <recommendations :peers="peersToStudy" />
                </md-tab>
            </md-tabs>
        </md-layout>
    </md-layout>
</template>



<style scoped>
    hr {
        border: none;
        border-bottom: 1px solid #ccc;
    }
    .fullHeight {
        height: 100%;
    }
    .headingContainer {
        margin: 8px 0px 0px 0px;
	}

    .md-tabs {
        border-top: 1px solid rgba(0, 0, 0, .12);
    }
	.competency {
        min-width: 100%;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .cardContainer {
        margin: 8px;
        flex: 1;
    }
    .peerCard {
        min-width: 40px;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .md-button {
      border-radius: 2px !important;
    }
    .questionCard .actions {
        justify-content: space-between;
    }
    .topicChip:hover {
        background-color: #333;
    }
    .placeAround {
        justify-content: space-between !important;
        display: flex;
        padding-bottom: 0px;
        align-items: center;
    }
    .placeAround > span {
        cursor: pointer;
    }
    .iconClass{
        align-items: center;
        background-color: red;
    }

    .cardPreview img {
        width: 50%;
        height: auto;
        float: left;
        border: 1px solid #bbb;
        padding-right: 10px;
        padding-bottom: 10px;
        margin-right: 10px;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle } from "av-ts";
    import PeerRepository from "@/repositories/PeerRepository";
    import AvailabilitySelector from "../util/AvailabilitySelector";
    import Recommendations from "./Recommendations";

    @Component({
        components: {
            "availability-selector": AvailabilitySelector,
            "recommendations": Recommendations
        }
    })
    export default class PeerView extends Vue {
        peersToMentor = {
            recommendations: PeerRepository.getMulti(3),
            requests: PeerRepository.getMulti(3)
        };

        peersToBeMentored = {
            recommendations: PeerRepository.getMulti(3),
            requests: PeerRepository.getMulti(3)
        };

        peersToStudy = {
            recommendations: PeerRepository.getMulti(3),
            requests: PeerRepository.getMulti(3)
        };
    }
</script>
