<template>
    <md-layout>
        <h1>Profile</h1>
        <md-tabs md-fixed
                 class="md-transparent">
            <md-tab md-label="Engagement">
            </md-tab>
            <md-tab md-label="Competencies">
            </md-tab>
            <md-tab md-label="Connections">
                <connectedness-heatmap :data="profileData"
                                       :topics="topics"
                                       :categories="categories">
                </connectedness-heatmap>
    
            </md-tab>
            <md-tab md-label="Achievements">
                <collected-badges></collected-badges>
            </md-tab>
        </md-tabs>
    </md-layout>
</template>

<style scoped>
    h1 {
        width: 100%;
    }
</style>

<script lang="ts">
    import { Vue, Component } from "av-ts";
    import UserRepository from "../../repositories/UserRepository";
    import ConnectednessHeatmap from "../util/ConnectednessHeatmap.vue";
    import CollectedBadges from "../util/CollectedBadges.vue";

    @Component({
        components: {
            "connectedness-heatmap": ConnectednessHeatmap,
            "collected-badges": CollectedBadges
        }
    })
    export default class DefaultView extends Vue {
        profileData = UserRepository.getLoggedInUser();

        get topics() {
            return UserRepository.getAllAvailableTopics();
        }

        get categories() {
            return UserRepository.getAllAvailableCategories();
        }
    }
</script>
