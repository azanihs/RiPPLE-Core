<template>
    <md-layout>
        <md-card class="fullWidth">
            <md-layout md-flex="100">
                <md-card class="componentSeparator">
                    <timeline events="connections"></timeline>
                </md-card>
            </md-layout>
            <md-layout md-flex="100">
                <md-card>
                    <h3>Current Connections</h3>
                    <current-connection-search :connections="connections">
                    </current-connection-search>
                </md-card>
            </md-layout>
        </md-card>
    </md-layout>
</template>

<style scoped>
.chartHeader {
    width: 100%;
    text-align: center;
    margin-top: 0px;
    color: #999;
}

.fullWidth {
    width: 100%;
    user-select: none;
    padding: 0px !important;
    overflow: hidden;
}

.overflowMobile {
    overflow: auto;
}

</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { IUser } from "../../interfaces/models";

import UserService from "../../services/UserService";

import CurrentConnectionSearch from "./CurrentConnectionSearch.vue";
import OverviewDescription from "../util/OverviewDescription.vue";
import Timeline from "../util/Timeline.vue";

@Component({
    components: {
        CurrentConnectionSearch,
        OverviewDescription,
        Timeline
    }
})
export default class Meetings extends Vue {

    pCurrentConnections: IUser[] = [];

    updateCurrentConnections(newConnections: IUser[]) {
        this.pCurrentConnections = newConnections;
    };

    @Lifecycle
    created() {
        UserService.getRecommendedConnections({ count: 3 }).then(this.updateCurrentConnections);
    }

    get connections() {
        return this.pCurrentConnections;
    }
}
</script>
