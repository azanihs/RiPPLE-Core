<template>
   <md-layout>
        <overview-description>
            <h2>Notifications Overview</h2>
            <p>The notifications overview shows you things which require your attention or action</p>
        </overview-description>
        <notifications></notifications>
    </md-layout>
</template>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";
import OverviewDescription from "../util/OverviewDescription.vue";
import Notifications from "../util/Notifications.vue";

@Component({
    components:{
        OverviewDescription,
        Notifications
    }
})
export default class NotificationsView extends Vue {
    
}
</script>
