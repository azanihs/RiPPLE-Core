<template>
<md-layout>
    <md-layout>
        <h2><md-icon>school</md-icon> {{ tabName }}</h2>
        <md-layout md-flex="100">
            No Data yet
        </md-layout>
    </md-layout>
    <md-layout md-flex="100">
        <h2><md-icon>people</md-icon> Recommendations</h2>
        <md-layout md-flex="100">
            <md-layout v-for="peer in peers.recommendations" :key="peer.id">
                <recommendation-card class="gutter" :data="peer" action="Request"/>
            </md-layout>
        </md-layout>
    </md-layout>
    <md-layout md-flex="100">
        <h2><md-icon>person_add</md-icon> Requests</h2>
        <md-layout md-flex="100">
            <md-layout v-for="peer in peers.requests" :key="peer.id">
                <recommendation-card class="gutter" :data="peer" action="Accept" />
            </md-layout>
        </md-layout>
    </md-layout>
</md-layout>
</template>

<style scoped>
.gutter {
    margin: 8px;
}
</style>

<script lang="ts">
    import { Vue, Component, Prop } from "av-ts";
    import RecommendationCard from "./RecommendationCard";

    @Component({
        components: {
            "recommendation-card": RecommendationCard
        }
    })
    export default class Recommendations extends Vue {
        @Prop peers;
        @Prop tabName: string;
    }
</script>

