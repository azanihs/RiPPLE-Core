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
import { Vue, Component } from "av-ts";

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
