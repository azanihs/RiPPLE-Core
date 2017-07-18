<template>
    <md-layout>
        <h3 :class="{'borderTop': separator}">{{topic}} Badges</h3>
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
    h3 {
        width: 100%;
        text-transform: capitalize;
    }
    
    h3:not(.borderTop) {
        padding-top: 0em;
        margin-top: 0em;
    }
    
    h3.borderTop {
        padding-top: 0.75em;
        border-top: 1px solid #ddd;
    }
    
    .badgeGutter {
        padding-left: 16px;
        padding-right: 16px;
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
    import UserRepository from "../../repositories/UserRepository";

    @Component({
        components: {
            "user-badge": UserBadge
        }
    })
    export default class CollectedBadges extends Vue {
        @Prop topic = p(String);
        @Prop separator = p({
            type: Boolean,
            default: true
        });

        get availableBadges() {
            const badges = UserRepository.getAllAvailableBadges();
            if (this.topic != "all") {
                return badges.filter(x => x.category == this.topic);
            }
            return badges;
        }
    }
</script>
