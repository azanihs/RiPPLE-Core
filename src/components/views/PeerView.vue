<template>
    <md-layout md-flex="95">
        <md-layout md-flex="100" class="headingContainer">
            <h1>Availability</h1>
            <availability-selector @change="shuffleData(null)"></availability-selector>
        </md-layout>
        <md-layout class="headingContainer">
            <h1>Connect To Peers</h1>
        </md-layout>
        <md-layout class="fullHeight" md-flex="100">
            <md-tabs md-fixed class="md-transparent" @change="tabChange">
                <md-tab v-for="tab in tabLookup" :key="tab.name" :md-label="tab.name">
                    <recommendations @change="shuffleData(tab.name)" :tabName="tab.heading" :peers="tab.data" :threshold="tab.name == 'Provide Mentorship' ? 75 : 0"></recommendations>
                </md-tab>
            </md-tabs>
        </md-layout>
    </md-layout>
</template>

<style scoped>
h1 {
    width: 100%;
}

.headingContainer {
    margin: 8px 0px 0px 0px;
}

.md-tabs {
    border-top: 1px solid rgba(0, 0, 0, .12);
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import UserService from "../../services/UserService";
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
        data: {}
    }, {
        name: "Seek Mentorship",
        heading: "seek mentorship in",
        data: {}
    }, {
        name: "Find Study Partners",
        heading: "find study partners In",
        data: {}
    }];

    @Lifecycle
    created() {
        this.shuffleData("all");
    }

    tabChange(newTabIndex: number) {
        this.tabID = newTabIndex;
        this.shuffleData(this.tabLookup[this.tabID].name);
    }

    shuffleData(type: string) {
        this.tabLookup[this.tabID].data = Object.assign({}, {
            recommendations: UserService.getRecommendedConnections(3),
            requests: UserService.getOutstandingRequests(3)
        });
    }
}
</script>
