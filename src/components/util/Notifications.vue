<template>
    <md-layout md-flex="100">
        <div class="notification"
             v-for="notification in notifications"
             :key="notification.id">
            <md-card md-with-hover
                     class="card"
                     :class="{disabled: notification.read}">
                <div class="leftPanel">
                    <md-icon>{{iconFromType(notification.type)}}</md-icon>
                </div>
                <div class="rightPanel">
                    <h3>{{notification.type}}</h3>
                    <p>{{notification.content}}</p>
                    <span class="date">{{ notificationDate }}</span>
                </div>
            </md-card>
        </div>
    </md-layout>
</template>

<style scoped>
h3 {
    color: #666;
    margin: 0px;
}

p {
    margin-top: 0.25em;
    margin-bottom: 0px;
}

p+p {
    margin-top: 1em;
}

.card {
    padding: 0px !important;
    flex-wrap: nowrap !important;
}

.leftPanel {
    padding: 16px;
    background-color: #fafafa;
    border-right: #eee;
    color: #256;
    justify-content: center;
}

.leftPanel i {
    height: 100%;
}

.rightPanel {
    padding: 16px;
}

.notification {
    margin-bottom: 1em;
    width: 100%;
}

.date {
    position: absolute;
    right: 16px;
    top: 16px;
    font-style: italic;
    color: #999;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Watch, Prop, p } from "av-ts";

import UserService from "../../services/UserService";
import Fetcher from "../../services/Fetcher";

@Component()
export default class Notifications extends Vue {
    @Prop
    showCount = p({
        type: Number,
        default: 10
    }) as number;

    pNotifications = [];
    updateNotifications(newNotifications) {
        this.pNotifications = newNotifications.slice(0, this.showCount);
    };

    date = new Date();

    @Lifecycle
    created() {
        Fetcher.get(UserService.getUserNotifications)
            .on(this.updateNotifications);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getUserNotifications)
            .off(this.updateNotifications);
    }

    get notificationDate() {
        return `${this.date.getFullYear()}`.slice(2, 4)
            + "/"
            + (this.date.getMonth() + 1)
            + "/" +
            this.date.getDate()
            + " "
            + this.date.getHours()
            + ":"
            + this.date.getMinutes();
    }

    get notifications() {
        return this.pNotifications;
    }

    iconFromType(notification) {
        return ({
            "Incoming Connection": "supervisor_account",
            "Achievement": "bar_chart",
            "Personal Goal": "trending_up",
            "Upcoming Meeting": "hourglass_full"
        })[notification];
    }
}
</script>
