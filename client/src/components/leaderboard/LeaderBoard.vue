<template>
    <md-table-card class="table">
        <md-table md-sort="reputation"
                  md-sort-type="asc"
                  @sort="sort">
            <md-table-header>
                <md-table-row>
                    <md-table-head>
                        <span>Rank</span>
                    </md-table-head>
                    <md-table-head>
                        <md-icon>camera_alt</md-icon>
                        <span>Avatar</span>
                    </md-table-head>
                    <md-table-head md-sort-by="name">
                        <md-icon>account_box</md-icon>
                        <span>Name</span>
                    </md-table-head>
                    <md-table-head md-sort-by="questionsAuthored">
                        <md-icon>library_add</md-icon>
                        <span>Questions Contributed</span>
                    </md-table-head>
                    <md-table-head md-sort-by="questionsAnswered">
                        <md-icon>reply</md-icon>
                        <span>Questions Answered</span>
                    </md-table-head>
                    <md-table-head md-sort-by="questionsAnsweredCorrectly">
                        <md-icon>check</md-icon>
                        <span>Answered Correctly</span>
                    </md-table-head>
                    <md-table-head md-sort-by="questionsRated">
                        <md-icon>star_rate</md-icon>
                        <span>Questions Rated</span>
                    </md-table-head>
                    <md-table-head md-sort-by="achievementsEarned">
                        <md-icon>gamepad</md-icon>
                        <span>Achievements Earned</span>
                    </md-table-head>
                </md-table-row>
            </md-table-header>
            <md-table-body>
                <md-table-row v-for="user in pagedUsers"
                              :key="user.id"
                              v-bind:class="{ userRow: user.id !== undefined }">
                    <md-table-cell>{{ user.rank }}</md-table-cell>
                    <md-table-cell>
                        <md-image class="avatar"
                                  :md-src="user.image"
                                  :alt="user.name"></md-image>
                    </md-table-cell>
                    <md-table-cell>{{ user.name }}</md-table-cell>
                    <md-table-cell>{{ user.questionsAuthored }}</md-table-cell>
                    <md-table-cell>{{ user.questionsAnswered }}</md-table-cell>
                    <md-table-cell>{{ user.questionsAnsweredCorrectly }}</md-table-cell>
                    <md-table-cell>{{ user.questionsRated }}</md-table-cell>
                    <md-table-cell>{{ user.achievementsEarned }}</md-table-cell>
                </md-table-row>
            </md-table-body>
        </md-table>
        <md-table-pagination ref="pagination"
                             :md-total="users.length"
                             :md-size="itemsPerPage"
                             :md-page="pageIndex"
                             @pagination="updateShowItems"></md-table-pagination>
    </md-table-card>
</template>

<style scoped>
.table {
    margin-top: 1em;
    flex-direction: column !important;
}

.avatar {
    width: 50px;
    height: 50px;
    border: 2px solid #ccc;
    box-shadow: 2px 2px 10px #888;
}

.userRow {
    font-weight: bold;
    background-color: #efefef;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { IUserSummary } from "../../interfaces/models";

import UserService from "../../services/UserService";

@Component()
export default class LeaderBoard extends Vue {

    itemsPerPage = 10;
    pageIndex = 1;

    sortType: string = "reputation";
    reverse: boolean = false;

    pUsers: IUserSummary[] = [];
    updateUsers(newUsers: IUserSummary[]) {
        this.pUsers = newUsers;
        this.$emit("userData", newUsers);
    };

    @Lifecycle
    created() {
        UserService.getMostReputableUsers({
            sortField: "questionsAuthored",
            sortOrder: "DESC"
        }).then(this.updateUsers);
    }

    updateShowItems(pageIndo: { size: number, page: number}) {
        this.itemsPerPage = pageIndo.size;
        this.pageIndex = pageIndo.page;
    }

    sort(item: { name: string, type: "DESC" | "ASC" }) {
        const sortOrder = item.type.toUpperCase() as "DESC" | "ASC";
        UserService.getMostReputableUsers({
            sortField: item.name,
            sortOrder: sortOrder
        }).then(this.updateUsers);
    }

    get users() {
        return this.pUsers;
    }

    get pagedUsers() {
        if (this.users !== undefined) {
            const users = this.users.slice(0 + this.itemsPerPage * (this.pageIndex - 1),
                (this.itemsPerPage * this.pageIndex));
            const ownUserIndex = users.findIndex(x => x.id !== undefined);
            const ownUser = this.users.find(x => x.id !== undefined);
            if (ownUserIndex === -1 && ownUser !== undefined && ownUser.rank < users[0].rank ) {
                users.unshift(ownUser);
            } else if (ownUserIndex === -1 && ownUser !== undefined) {
                const joinedUsers = users.concat(ownUser);
                return joinedUsers;
            }
            return users;
        }
    }
}
</script>
