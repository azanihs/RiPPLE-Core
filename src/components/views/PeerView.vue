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
                <md-tab md-label="Provide Mentorship">
                    <recommendations tabName="Provide Mentorship In" :peers="peersToMentor" />
                </md-tab>
                <md-tab md-label="Seek Mentorship">
                    <recommendations tabName="Seek Mentorship In" :peers="peersToBeMentored" />
                </md-tab>
                <md-tab md-label="Find Study Partners">
                    <recommendations tabName="Find Study Partners In" :peers="peersToStudy" />
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
