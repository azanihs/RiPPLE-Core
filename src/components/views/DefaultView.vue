<template>
    <connectedness-heatmap :data="profileData"
                           :topics="topics"
                           :categories="categories">
    </connectedness-heatmap>
</template>

<style scoped>
    
</style>

<script lang="ts">
    import { Vue, Component } from "av-ts";
    import UserRepository from "../../repositories/UserRepository";
    import ConnectednessHeatmap from "../util/ConnectednessHeatmap.vue";

    @Component({
        components: {
            "connectedness-heatmap": ConnectednessHeatmap
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
