<template>
    <div class="badgeContainer"
        :class="{obtained: userHasBadge, progress: userHasStartedBadge}">
        <div class="badgeProgress">
            <div class="badge">
                <md-icon>{{badgeIcon}}</md-icon>
            </div>
            <md-spinner v-if="badge.progress >= 0"
                        md-theme="spinner"
                        class="badgeSpinner"
                        :md-stroke="4"
                        :md-progress="100"></md-spinner>
            <md-spinner v-if="badge.progress >= 0"
                        class="progressSpinner badgeSpinner"
                        :md-stroke="4"
                        :md-progress="badge.progress"></md-spinner>
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

.badgeContainer:not(.obtained) {
    color: #bbb;
}

.badge {
    padding: 0.5em;
}

.obtained .badgeProgress {
    padding: 0px 1em;
}

.obtained .badge {
    color: #ffcc00;
    background-color:#256;
    border-radius: 50%;
    border: 0.3em solid #256;
}

.obtained .md-spinner {
    width: 0px !important;
}

.badgeContainer:not(.obtained).progress, .badgeContainer:not(.obtained):hover {
    color: #256;
}

</style>

<script lang="ts">
import { Vue, Prop, Component, p } from "av-ts";

import { Badge } from "../../interfaces/models";
import BadgeService from "../../services/BadgeService";

@Component()
export default class Badges extends Vue {
    @Prop badge = p<Badge>({
        required: true
    });

    get badgeIcon() {
        return BadgeService.badgeToIcon(this.badge);
    }

    get userHasBadge(): boolean {
        return this.badge.progress == 100;
    }

    get userHasStartedBadge(): boolean {
        return this.badge.progress > 0;
    }
}
</script>
