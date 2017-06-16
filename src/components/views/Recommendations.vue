<template>
<md-list md-expand-multiple>
    <md-list-item>
        <md-icon>school</md-icon>
        <span>COMPETENCIES</span>
        <md-list-expand>
            <md-layout md-gutter="16" md-flex="100">
                No Data yet
            </md-layout>
        </md-list-expand>
    </md-list-item>
    <md-list-item>
        <md-icon>people</md-icon>
        <span>RECOMMENDATIONS</span>
        <md-list-expand>
            <md-layout md-flex="100">
                <md-layout v-for="peer in peers.recommendations" :key="peer.id">
                    <recommendation-card :data="peer"/>
                </md-layout>
            </md-layout>
        </md-list-expand>
    </md-list-item>
    <md-list-item>
        <md-icon>person_add</md-icon>
        <span>REQUESTS</span>
        <md-list-expand>
            <md-layout md-gutter="16" md-flex="100">
                <md-layout v-for="peer in peers.requests" :key="peer.id">
                    <recommendation-card :data="peer" />
                </md-layout>
            </md-layout>
        </md-list-expand>
    </md-list-item>
</md-list>
</template>

<style scoped>
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
    }
</script>

