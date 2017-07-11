<template>
    <md-layout>
        <h2>Available Badges</h2>
        <md-button v-for="badge in availableBadges"
                   :key="badge.id"
                   class="badgeIcon"
                   :class="{'obtained': userBadges.find(x => x.badgeId == badge.id)}">
            <md-icon>{{getBadgeIcon(badge)}}</md-icon>
            <md-tooltip md-delay="50"
                        md-direction="top">{{badge.description}}</md-tooltip>
        </md-button>
    </md-layout>
</template>

<style scoped>
    h2 {
        width: 100%;
        padding-top: 0.5em;
        border-top: 1px solid #ccc
    }
    
    .badgeIcon {
        color: #ccc;
    }
    
    .obtained {
        color: #256;
    }
</style>

<script lang="ts">
    import { Vue, Prop, Lifecycle, Component } from "av-ts";
    import BadgeService from "../../services/BadgeService";
    import UserRepository from "../../repositories/UserRepository";

    @Component()
    export default class CollectedBadges extends Vue {
        get availableBadges() {
            return UserRepository.getAllAvailableBadges();
        }

        get userBadges() {
            return UserRepository.getAllUserBadges();
        }

        getBadgeIcon(badge) {
            return BadgeService.badgeToIcon(badge);
        }
    }
</script>
