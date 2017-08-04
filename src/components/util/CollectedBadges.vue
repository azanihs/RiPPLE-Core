<template>
    <md-card class="card">
        <md-layout>
            <h3>{{topic}} Badges</h3>
            <md-layout v-for="badge in availableBadges" :key="badge.id" md-flex="33" class="badgeGutter" md-gutter>
                <user-badge :badge="badge"></user-badge>
            </md-layout>
        </md-layout>
    </md-card>
</template>

<style scoped>
.card {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    flex: 1;
    padding: 16px;
}

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
import { Vue, Prop, Lifecycle, Component, p } from "av-ts";
import UserBadge from "../util/UserBadge.vue";
import BadgeService from "../../services/BadgeService";

@Component({
    components: {
        "user-badge": UserBadge
    }
})
export default class CollectedBadges extends Vue {
    @Prop topic = p(String);

    get availableBadges() {
        const badges = BadgeService.getAllAvailableBadges();
        if (this.topic != "all") {
            return badges.filter(x => x.category == this.topic);
        }
        return badges;
    }
}
</script>
