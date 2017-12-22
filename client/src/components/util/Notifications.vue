<template>
    <md-layout v-if="notifications.length > 0" md-flex="100" class="column">
        <div class="notification"
             v-for="notification in notifications"
             :key="notification.id">

            <md-card md-with-hover
                     class="card"
                     :class="{disabled: notification.read}">
                <div class="leftPanel">
                    <md-icon>{{notification.icon}}</md-icon>
                </div>

                <div class="rightPanel"
                :class="{'mobileStyle': mobileMode}">
                    <h3>{{notification.name}}</h3>
                    <p>{{notification.description}}</p>
                    <span class="date">{{ notificationDate(notification) }}</span>
                </div>

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

.column {
    flex-direction:column;
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
import { Vue, Component, Lifecycle, Prop, p, Mixin as mixin } from "av-ts";
import { INotification } from "../../interfaces/models";

import UserService from "../../services/UserService";
import responsiveMixin from "../../responsiveMixin";
import Fetcher from "../../services/Fetcher";
import { serverToLocal } from "../../util";

@Component
export default class Notifications extends mixin(responsiveMixin, Vue) {
    @Prop
    showCount = p<number>({
        default: 10
    });

    pNotifications: INotification[] = [];
    updateNotifications(newNotifications: INotification[]) {
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

    notificationDate(notification: INotification) {
        return serverToLocal(<number> notification.created);
    }

    get notifications() {
        return this.pNotifications;
    }
}
</script>
