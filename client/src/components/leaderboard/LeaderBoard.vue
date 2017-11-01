<template>
    <md-table-card class="table">
        <md-table md-sort="reputation"
                  md-sort-type="asc"
                  @sort="sort">
            <md-table-header>
                <md-table-row>
                    <md-table-head>
                        <md-icon>camera_alt</md-icon>
                        <span>Avatar</span>
                    </md-table-head>
                    <md-table-head md-sort-by="name">
                        <md-icon>account_box</md-icon>
                        <span>Name</span>
                    </md-table-head>
                    <md-table-head md-sort-by="reputation">
                        <md-icon>star</md-icon>
                        <span>Reputation</span>
                    </md-table-head>
                    <md-table-head md-sort-by="questionsContributed">
                        <md-icon>library_add</md-icon>
                        <span>Questions Contributed</span>
                    </md-table-head>
                    <md-table-head md-sort-by="numberAnswers">
                        <md-icon>reply</md-icon>
                        <span>Questions Answered</span>
                    </md-table-head>
                    <md-table-head md-sort-by="numberComments">
                        <md-icon>message</md-icon>
                        <span>Comments</span>
                    </md-table-head>
                </md-table-row>
            </md-table-header>
            <md-table-body>
                <md-table-row v-for="user in sortedUsers"
                              :key="user.id">
                    <md-table-cell>
                        <md-image class="avatar"
                                  :md-src="user.image"
                                  :alt="user.name"></md-image>
                    </md-table-cell>
                    <md-table-cell>{{ user.name }}</md-table-cell>
                    <md-table-cell>{{ user.reputation }}</md-table-cell>
                    <md-table-cell>{{ user.questionsContributed }}</md-table-cell>
                    <md-table-cell>{{ user.numberAnswers }}</md-table-cell>
                    <md-table-cell>{{ user.numberComments }}</md-table-cell>
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
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import UserService from "../../services/UserService";
import Fetcher from "../../services/Fetcher";

@Component()
export default class LeaderBoard extends Vue {

    itemsPerPage = 10;
    pageIndex = 1;

    sortType: string = "";
    reverse: boolean = false;

    pUsers = [];
    updateUsers(newUsers) {
        this.pUsers = newUsers;
    };

    @Lifecycle
    created() {
        // TODO: Ew. Pagination component does not update totalItems on mount.
        this.$nextTick(() => {
            //this.$refs["pagination"]["totalItems"] = this.users.length;
        });

        Fetcher.get(UserService.mostReputableUsers)
            .on(this.updateUsers);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.mostReputableUsers)
            .off(this.updateUsers);
    }

    updateShowItems(a) {
        this.itemsPerPage = a.size;
        this.pageIndex = a.page;
    }

    sort(item) {
        this.sortType = item.name;
        this.reverse = item.type == "desc";
    }

    get users() {
        return this.pUsers;
    }

    get sortedUsers() {
        const users = this.users;
        const sortKey = this.sortType || "reputation";

        const sortMethod = (a, b) => {
            if (Number.isNaN(+a[sortKey])) {
                return a[sortKey].localeCompare(b[sortKey]);
            }
            return a[sortKey] - b[sortKey];
        };

        const sortedUsers = this.reverse ? users.sort().reverse() : users.sort(sortMethod);
        const startIndex = (this.pageIndex - 1) * this.itemsPerPage;
        return sortedUsers.slice(startIndex, startIndex + this.itemsPerPage);
    }
}
</script>
