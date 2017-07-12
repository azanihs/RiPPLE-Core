<template>
    <md-layout md-gutter="16">
        <h2>Available Badges</h2>
        <md-layout v-for="badge in availableBadges"
                   :key="badge.id"
                   md-flex="33"
                   class="badgeGutter"
                   md-gutter>
            <div class="badgeContainer">
                <div class="badgeProgress"
                     :class="{obtained: getUserBadge(badge)}">
                    <md-icon>{{getBadgeIcon(badge)}}</md-icon>
                    <md-spinner v-if="getUserBadge(badge) && getUserBadge(badge).progress >= 0"
                                class="badgeSpinner"
                                :md-stroke="2"
                                :md-progress="getUserBadge(badge).progress"></md-spinner>
                </div>
                <div class="badgeDescription">
                    <h4>{{badge.name}}</h4>
                    <p>{{badge.description}}</p>
                </div>
            </div>
        </md-layout>
    </md-layout>
</template>

<style>
    .badgeProgress svg circle {
        /* TODO: Move to theme */
        stroke: #1d323a !important;
    }
</style>
<style scoped>
    h2 {
        width: 100%;
        padding-top: 0.75em;
        border-top: 1px solid #ccc
    }
    
    .badgeGutter:nth-of-type(3n + 1) {
        padding-left: 0px !important;
    }
    
    .badgeGutter:nth-of-type(3n) {
        padding-right: 0px !important;
    }
    
    .badgeContainer {
        display: flex;
        width: 100%;
        align-items: center;
        background-color: #fafafa;
        margin-bottom: 16px;
    }
    
    .badgeProgress {
        position: relative;
        height: 100%;
        background-color: #eee;
        align-items: center;
        display: flex;
        padding: 0px 1.25em;
        border-right: 1px solid #e1e1e1;
    }
    
    .badgeSpinner {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    
    .badgeDescription {
        padding-left: 8px;
    }
    
    .badgeDescription h4 {
        text-transform: capitalize;
        margin-bottom: 0px;
    }
    
    .badgeDescription p {
        margin-top: 0.5em;
    }
    
    .badgeProgress:not(.obtained) {
        color: #ddd;
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

        getUserBadge(badge) {
            return this.userBadges.find(x => x.badgeId == badge.id);
        }
    }
</script>
