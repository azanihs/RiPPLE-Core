<template>
    <div class="badgeContainer">
        <div class="badgeProgress"
             :class="{obtained: userHasBadge, progress: userHasStartedBadge}">
            <div class="badge">
                <md-icon>{{badgeIcon}}</md-icon>
            </div>
            <md-spinner v-if="userBadge && userBadge.progress >= 0"
                        md-theme="spinner"
                        class="badgeSpinner"
                        :md-stroke="2"
                        :md-progress="100"></md-spinner>
            <md-spinner v-if="userBadge && userBadge.progress >= 0"
                        class="progressSpinner badgeSpinner"
                        :md-stroke="2"
                        :md-progress="userBadge.progress"></md-spinner>
        </div>
        <div class="badgeDescription">
            <h4>{{badge.name}}</h4>
            <p>{{badge.description}}</p>
        </div>
    </div>
</template>

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

.badge {
    padding: 0.5em;
}

.obtained .badge {
    color: #f2f2f2;
    background-color: #256;
    border-radius: 50%;
}

.badgeProgress:not(.obtained).progress {
    color: #256;
}
</style>

<script lang="ts">
import { Vue, Prop, Lifecycle, Mixin, Watch, Component, p } from "av-ts";
import PropUpdate from "../mixins/PropUpdate";

import { AcquiredBadge, Badge } from "../../interfaces/models";
import BadgeService from "../../services/BadgeService";
import Fetcher from "../../services/Fetcher";

@Component()
export default class UserBadge extends PropUpdate {
    @Prop badge = p({
        required: true
    }) as Badge;

    pUserBadge = undefined;

    updateBadge(userBadge) {
        this.pUserBadge = userBadge;
    };

    @Lifecycle
    created() {
        Fetcher.get(BadgeService.userHasBadge, { badgeId: this.badge.id })
            .on(this.updateBadge);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(BadgeService.userHasBadge, { badgeId: this.badge.id })
            .off(this.updateBadge);
    }

    get badgeIcon() {
        return BadgeService.badgeToIcon(this.badge);
    }

    get userBadge(): AcquiredBadge {
        return this.pUserBadge;
    }

    get userHasBadge(): boolean {
        const badge = this.userBadge;
        if (badge === undefined) {
            return false;
        }

        // User only has the badge if they have met all criteria
        if (badge.progress >= 0) {
            return badge.progress == 100;
        }
        // User has the badge and it does not have a progress
        return true;
    }

    get userHasStartedBadge(): boolean {
        const badge = this.userBadge;
        if (badge === undefined) {
            return false;
        }

        // User only has the badge if they have met all criteria
        if (badge.progress >= 0) {
            return true;
        }
    }
}
</script>
