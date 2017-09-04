<template>
    <md-card>
        <md-layout>
            <h3>{{topic}} Badges</h3>
            <md-layout v-for="badge in availableBadges"
                       :key="badge.id"
                       md-flex="33"
                       class="badgeGutter"
                       md-gutter>
                <user-badge :badge="badge"></user-badge>
            </md-layout>
        </md-layout>
    </md-card>
</template>

<style scoped>
h3 {
    width: 100%;
    margin-top: 0px;
    text-transform: capitalize;
}

.badgeGutter {
    padding-left: 8px;
    padding-right: 8px;
}

.badgeGutter:nth-of-type(3n + 1) {
    padding-left: 0px !important;
}

.badgeGutter:nth-of-type(3n) {
    padding-right: 0px !important;
}
</style>

<script lang="ts">
import { Vue, Prop, Lifecycle, Mixin, Watch, Component, p } from "av-ts";
import { Badge } from "../../interfaces/models";
import PropUpdate from "../mixins/PropUpdate";
import UserBadge from "../util/UserBadge.vue";
import BadgeService from "../../services/BadgeService";
import Fetcher from "../../services/Fetcher";


@Component({
    components: {
        "user-badge": UserBadge
    }
})
export default class CollectedBadges extends PropUpdate {
    @Prop topic = p(String);

    availableBadges = [];
    fetcherInstance = undefined;

    updateAvailableBadges(newBadges) {
        this.availableBadges = newBadges;
    };

    @Lifecycle
    created() {
        if (this.topic == "all") {
            this.fetcherInstance = Fetcher.get(BadgeService.getAllAvailableBadges);
        } else if (this.topic == "closest") {
            this.fetcherInstance = Fetcher.get(BadgeService.getClosestUserBadges);
        } else {
            this.fetcherInstance = Fetcher.get(BadgeService.getBadgesByCategory, { category: this.topic });
        }

        this.fetcherInstance.on(this.updateAvailableBadges);
        this.fetcherInstance.run();
    }

    @Lifecycle
    destroyed() {
        if (this.fetcherInstance !== undefined) {
            this.fetcherInstance.off(this.updateAvailableBadges);
        }
    }

}
</script>
