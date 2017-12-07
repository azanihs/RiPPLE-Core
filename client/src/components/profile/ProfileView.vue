<template>
    <md-layout>
        <md-layout md-flex="100"
            class="componentSeparator overview">
            <md-layout class="notificationSummary">
                <h2>Notifications</h2>
            </md-layout>
            <md-layout class="engagementSummary">
                <h2>Engagement</h2>
            </md-layout>

            <md-layout class="notificationSummary">
                <notifications :showCount="10"></notifications>
            </md-layout>
            <md-layout class="engagementSummary">
                <md-card v-for="item in engagementSummary"
                    :key="item.node.id"
                    class="engagementItem">
                    <h3>{{item.node.name}}</h3>
                    <div class="engagementScore">
                        <div class="engagementButton">
                            {{item.score}}
                        </div>
                        <md-spinner md-theme="spinner"
                            class="engagementScoreProgress"
                            :md-stroke="4"
                            :md-progress="100"></md-spinner>
                        <md-spinner class="progressSpinner engagementScoreProgress"
                            :md-stroke="4"
                            :md-progress="item.score"></md-spinner>
                    </div>
                </md-card>
            </md-layout>
        </md-layout>
        <collected-badges topic='closest'></collected-badges>
    </md-layout>
</template>

<style scoped>
.overview {
    align-items: stretch;
}

.notificationSummary {
    align-items: stretch;
    min-width: 48.75%;
    flex: 0 1 48.75%;
}

.engagementSummary {
    align-items: stretch;
    min-width: 48.75%;
    flex: 0 1 48.75%;
    margin-left: 2.5%;
}

h2 {
    width: 100%;
}

.engagementItem {
    flex: none !important;
    width: 47.5%;
    padding: 1em;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #f9f9f9;
    border: 1px solid #f2f2f2;
    overflow: hidden;
}

.engagementItem:nth-child(odd) {
    margin-right: 2.5%;
}

.engagementItem:nth-child(even) {
    margin-left: 2.5%;
}

h3 {
    width: 100%;
}

.engagementItem h3 {
    display: block;
    width: 100%;
    margin: 0px 0px 0.5em 0px;
    text-align: center;
}

.engagementScore {
    position: relative;
    text-align: center;
    left: 50%;
    height: 50px;
}

.engagementScore::after {
    content: "\00a0";
}

.engagementButton {
    font-size: 1.5em;
    background-color: transparent !important;
    color: #256 !important;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.engagementScoreProgress {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { IUser, ITopic } from "../../interfaces/models";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";

import CollectedBadges from "../util/CollectedBadges.vue";
import Notifications from "../util/Notifications.vue";

interface IEngagementSummary {
    node: ITopic,
    score: number
};

@Component({
    components: {
        Notifications,
        CollectedBadges
    }
})
export default class DefaultView extends Vue {

    pUser: IUser | undefined = undefined;
    pEngagementSummary: IEngagementSummary[] = [];

    updateEngagementSummary(newSummary: IEngagementSummary[]) {
        this.pEngagementSummary = newSummary;
    };

    updateUser(user: IUser) {
        this.pUser = user;
    };


    @Lifecycle
    created() {
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateUser);
        Fetcher.get(UserService.getEngagementSummary)
            .on(this.updateEngagementSummary);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateUser);
        Fetcher.get(UserService.getEngagementSummary)
            .off(this.updateEngagementSummary);
    }

    get profileData() {
        return this.pUser;
    }

    get engagementSummary() {
        return this.pEngagementSummary;
    }

}
</script>
