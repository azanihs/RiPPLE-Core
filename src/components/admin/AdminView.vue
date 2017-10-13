<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100">
            <md-card>
                <h2>Administration Page for: {{courseCode}}</h2>

                <md-input-container>
                    <label>Teaching Start</label>
                    <md-input v-model="teachingStart"></md-input>
                </md-input-container>
                <md-input-container>
                    <label>Teaching End</label>
                    <md-input v-model="teachingEnd"></md-input>
                </md-input-container>
                <md-chips v-model="topics"
                          md-input-placeholder="Course Topics"></md-chips>
            </md-card>
        </md-layout>
        <leader-board></leader-board>
        <md-layout md-flex="100">
            <md-card>
                <md-button class="md-raised">Download Spreadsheet Results</md-button>
                <md-button class="md-raised">Download Database Dump</md-button>
            </md-card>
        </md-layout>
        <md-dialog ref="course_create_modal"
                   :md-click-outside-to-close="false"
                   :md-esc-to-close="false">
            <md-dialog-title>Create new course</md-dialog-title>
            <md-dialog-content>
                <p>Your course: {{courseCode}} does not appear to exist.</p>
                <p> Would you like to create it?</p>
            </md-dialog-content>
            <md-dialog-content>
                <form>
                    <md-input-container>
                        <label>Course Code</label>
                        <md-input v-model="courseCode"></md-input>
                    </md-input-container>
                </form>
            </md-dialog-content>

            <md-dialog-actions>
                <md-button class="md-primary"
                           @click="closeDialog()">Create</md-button>
            </md-dialog-actions>
        </md-dialog>
    </md-layout>
</template>

<style scoped>

</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { User, Course } from "../../interfaces/models";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";

import LeaderBoard from "../leaderboard/LeaderBoard.vue";

const _MODAL_NAME = "course_create_modal";

@Component({
    components: {
        LeaderBoard
    }
})
export default class AdminView extends Vue {
    topics = [];
    courseCode = "";
    teachingStart = new Date().toUTCString();
    teachingEnd = "";

    pUser: User = undefined;
    pCourse: Course = undefined;

    updateUserCourse(courseUser: { user: User, course: Course }) {
        console.log(courseUser);

        this.pUser = courseUser.user;
        this.pCourse = courseUser.course;

        this.courseCode = this.pCourse.courseCode;
        this.openDialog();
    }

    @Lifecycle
    created() {
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateUserCourse);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateUserCourse);
    }

    openDialog() {
        (this.$refs[_MODAL_NAME] as any).open();
    };
    closeDialog() {
        (this.$refs[_MODAL_NAME] as any).close();
    };
}
</script>
