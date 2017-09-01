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
import PropUpdate from "../mixins/PropUpdate";
import UserBadge from "../util/UserBadge.vue";
import BadgeService from "../../services/BadgeService";

@Component({
    components: {
        "user-badge": UserBadge
    }
})
export default class CollectedBadges extends PropUpdate {
    @Prop topic = p(String);

    availableBadges = [];

    @Lifecycle
    created() {
        let subscription = undefined;
        let param = undefined;

        if (this.topic == "all") {
            subscription = BadgeService.getAllAvailableBadges;
        } else if (this.topic == "closest") {
            subscription = BadgeService.getClosestUserBadges;
        } else {
            subscription = BadgeService.getBadgeByType;
            param = this.topic;
        }
        BadgeService.subscribe(subscription, param, this.updateProp("availableBadges"));
    }

}
</script>
