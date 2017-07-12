<template>
    <div class="badgeContainer">
        <div class="badgeProgress"
             :class="{obtained: !!userBadge}">
            <md-icon>{{badgeIcon}}</md-icon>
            <md-spinner v-if="userBadge && userBadge.progress >= 0"
                        class="badgeSpinner"
                        :md-stroke="2"
                        :md-progress="userBadge.progress"></md-spinner>
        </div>
        <div class="badgeDescription">
            <h4>{{badge.name}}</h4>
            <p>{{badge.description}}</p>
        </div>
    </div>
</template>

<style>
    .badgeProgress svg circle {
        /* TODO: Move to theme */
        stroke: #1d323a !important;
    }
</style>
<style scoped>
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
    import { AcquiredBadge, Badge } from "../../interfaces/models";
    import BadgeService from "../../services/BadgeService";
    import UserRepository from "../../repositories/UserRepository";

    @Component()
    export default class UserBadge extends Vue {
        @Prop badge: Badge;

        get badgeIcon() {
            return BadgeService.badgeToIcon(this.badge);
        }

        get userBadge(): AcquiredBadge {
            // TODO: This lookup is very slow, a hashmap or similar would be better.
            return UserRepository.getAllUserBadges().find(x => x.badgeId == this.badge.id);
        }
    }
</script>
