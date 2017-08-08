<template>
    <md-table-card class="table">
        <md-table>
            <md-table-header>
                <md-table-row>
                    <md-table-head>
                        <md-icon>account_box</md-icon>
                        <span>Name</span>
                    </md-table-head>
                    <md-table-head>
                        <md-icon>star</md-icon>
                        <span>Reputation</span>
                    </md-table-head>
                    <md-table-head>
                        <md-icon>library_add</md-icon>
                        <span>Questions Contributed</span>
                    </md-table-head>
                    <md-table-head>
                        <md-icon>reply</md-icon>
                        <span>Questions Answered</span>
                    </md-table-head>
                    <md-table-head>
                        <md-icon>message</md-icon>
                        <span>Comments</span>
                    </md-table-head>
                </md-table-row>
            </md-table-header>
            <md-table-body>
                <md-table-row v-for="user in mostReputableUsers" :key="user.id">
                    <md-table-cell>{{ user.name }}</md-table-cell>
                    <md-table-cell>{{ user.reputation }}</md-table-cell>
                    <md-table-cell>{{ user.questionsContributed }}</md-table-cell>
                    <md-table-cell>{{ user.numberAnswers }}</md-table-cell>
                    <md-table-cell>{{ user.numberComments }}</md-table-cell>
                </md-table-row>
            </md-table-body>
        </md-table>
    </md-table-card>
</template>

<style scoped>
.table {
    margin-top: 1em;
    flex-direction: column !important;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import UserService from "../../services/UserService";

@Component()
export default class LeaderBoard extends Vue {

    get mostReputableUsers() {
        return UserService.mostReputableUsers();
    }
}
</script>
