<template>
    <div>
        <connectedness-heatmap :data="profileData"
                               :topics="topics"
                               :categories="categories">
        </connectedness-heatmap>
        <collected-badges></collected-badges>
    </div>
</template>

<style scoped>
    
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
