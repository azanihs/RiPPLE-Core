<template>
    <md-layout v-if="notifications.length > 0" md-flex="100">
        <div class="notification"
             v-for="notification in notifications"
             :key="notification.id">

            <md-card md-with-hover
                     class="card"
                     :class="{disabled: notification.read}">
                <div class="leftPanel">
                    <md-icon>{{notification.icon}}</md-icon>
                </div>

            <responsive-wrapper class="rightPanel">
                <div>
                    <h3>{{notification.name}}</h3>
                    <p>{{notification.description}}</p>
                    <span class="date">{{ notificationDate }}</span>
                </div>
             </responsive-wrapper>

            </md-card>
        </div>
    </md-layout>
    <md-layout v-else md-flex="100">
        <md-card class="centre">
            <div class="content">
                <h2>No notifications available</h2>
                <md-icon>alarm</md-icon>
            </div>
        </md-card>
    </md-layout>
</template>

<style scoped>

.mobileStyle span{
    position: initial;
}

.centre {
    justify-content: center;
    align-items: center;
    text-align: center;
}
.content > h2,
.content > i {
    color: #ccc;
}
h3 {
    color: #666;
    margin: 0px;
}

p {
    margin-top: 0.25em;
    margin-bottom: 0px;
    margin-bottom: 0.3em;
}

p + p {
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
    padding-bottom: 5px;
    display: block;
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
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import { Notification } from "../../interfaces/models";
import ResponsiveWrapper from "../util/ResponsiveWrapper.vue";

import UserService from "../../services/UserService";
import Fetcher from "../../services/Fetcher";

@Component({
    components: {
        ResponsiveWrapper
    }
})
export default class Notifications extends Vue {
    @Prop
    showCount = p<number>({
        default: 10
    });

    pNotifications: Notification[] = [];
    updateNotifications(newNotifications: Notification[]) {
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
}
</script>
