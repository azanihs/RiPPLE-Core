<template>
    <md-layout md-flex="95">
        <md-layout md-flex="100" class="headingContainer">
            <h1>Availability</h1>
            <availability-selector @change="shuffleData" />
        </md-layout>
        <md-layout class="headingContainer">
            <h1>Connect To Peers</h1>
        </md-layout>
        <md-layout class="fullHeight" md-flex="100">
            <md-tabs md-fixed class="md-transparent">
                <md-tab md-label="Provide Mentorship">
                    <recommendations @change="shuffleData" tabName="Provide Mentorship In" :peers="peersToMentor" :threshold="75" />
                </md-tab>
                <md-tab md-label="Seek Mentorship">
                    <recommendations @change="shuffleData" tabName="Seek Mentorship In" :peers="peersToBeMentored" />
                </md-tab>
                <md-tab md-label="Find Study Partners">
                    <recommendations @change="shuffleData" tabName="Find Study Partners In" :peers="peersToStudy" />
                </md-tab>
            </md-tabs>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .headingContainer {
        margin: 8px 0px 0px 0px;
	}

    .md-tabs {
        border-top: 1px solid rgba(0, 0, 0, .12);
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

        peersToMentor = {};
        peersToBeMentored = {};
        peersToStudy = {};

        @Lifecycle
        created() {
            this.shuffleData();
        }

        shuffleData() {
            this.peersToMentor = {
                recommendations: PeerRepository.getMulti(3),
                requests: PeerRepository.getMulti(3)
            };

            this.peersToBeMentored = {
                recommendations: PeerRepository.getMulti(3),
                requests: PeerRepository.getMulti(3)
            };

            this.peersToStudy = {
                recommendations: PeerRepository.getMulti(3),
                requests: PeerRepository.getMulti(3)
            };
        }
    }
</script>
