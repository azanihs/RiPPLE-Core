<template>
    <md-layout md-flex="95">
        <md-layout md-flex="100"
                   class="headingContainer">
            <h1>Availability</h1>
            <availability-selector @change="shuffleData(null)"></availability-selector>
        </md-layout>
        <md-layout class="headingContainer">
            <h1>Connect To Peers</h1>
        </md-layout>
        <md-layout class="fullHeight"
                   md-flex="100">
            <md-tabs md-fixed
                     class="md-transparent"
                     @change="tabChange">
                <md-tab v-for="tab in tabLookup"
                        :key="tab.id"
                        :md-label="tab.name">
                    <recommendations @change="shuffleData(tab.id)"
                                     :tabName="tab.heading"
                                     :peers="tab.data"
                                     :threshold="75"></recommendations>
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
    import PeerRepository from "../../repositories/PeerRepository";
    import AvailabilitySelector from "../util/AvailabilitySelector.vue";
    import Recommendations from "./Recommendations.vue";

    @Component({
        components: {
            "availability-selector": AvailabilitySelector,
            "recommendations": Recommendations
        }
    })
    export default class PeerView extends Vue {

        tabID = 0;
        tabLookup = [{
            name: "Provide Mentorship",
            heading: "provide mentorship in",
            data: {},
            id: "peersToMentor"
        }, {
            name: "Seek Mentorship",
            heading: "seek mentorship in",
            data: {},
            id: "peersToBeMentored"
        }, {
            name: "Find Study Partners",
            heading: "find study partners In",
            data: {},
            id: "peersToStudy"
        }];

        @Lifecycle
        created() {
            this.shuffleData("all");
        }

        tabChange(newTabIndex: number) {
            this.tabID = newTabIndex;
            this.shuffleData(this.tabLookup[this.tabID].id);
        }

        shuffleData(type: string) {
            this.tabLookup[this.tabID].data = Object.assign({}, {
                recommendations: PeerRepository.getMany(3),
                requests: PeerRepository.getMany(3)
            });
        }
    }
</script>
