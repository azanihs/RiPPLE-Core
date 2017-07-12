<template>
    <md-layout md-gutter="16">
        <h2>Available Badges</h2>
        <md-layout v-for="badge in availableBadges"
                   :key="badge.id"
                   md-flex="33"
                   class="badgeGutter"
                   md-gutter>
            <user-badge :badge="badge"></user-badge>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    h2 {
        width: 100%;
        padding-top: 0.75em;
    }
    
    .badgeGutter:nth-of-type(3n + 1) {
        padding-left: 0px !important;
    }
    
    .badgeGutter:nth-of-type(3n) {
        padding-right: 0px !important;
    }
</style>

<script lang="ts">
    import { Vue, Prop, Lifecycle, Component } from "av-ts";
    import UserBadge from "../util/UserBadge.vue";
    import BadgeService from "../../services/BadgeService";
    import UserRepository from "../../repositories/UserRepository";

    @Component({
        components: {
            "user-badge": UserBadge
        }
    })
    export default class CollectedBadges extends Vue {
        get availableBadges() {
            return UserRepository.getAllAvailableBadges();
        }
    }
</script>
