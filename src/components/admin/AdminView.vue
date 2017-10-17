<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100">
            <md-card>
                <h2>Administration Page for: {{courseCode}}</h2>
                <md-input-container>
                    <label>Teaching Start: {{this.teachingStart}}</label>
                    <date-picker v-model="teachingStart"></date-picker>
                </md-input-container>
                <md-input-container>
                    <label>Teaching End: {{this.teachingEnd}}</label>
                    <date-picker v-model="teachingEnd"></date-picker>
                </md-input-container>
                <div>
                    <topic-chip v-for="topic in topics"
                        :key="topic.id">{{topic.name}}</topic-chip>
                </div>
                <md-button class="md-fab md-primary"
                    :disabled="courseIsAvailable">
                    <md-icon>save</md-icon>
                </md-button>
            </md-card>
        </md-layout>
        <leader-board class="componentSeparator"
            v-if="courseIsAvailable"></leader-board>
        <md-layout v-if="courseIsAvailable"
            class="componentSeparator"
            md-flex="100">
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
            </md-dialog-content>
            <md-dialog-content>
                <span>{{networkError}}</span>
                <form>
                    <md-input-container>
                        <label>Course Code</label>
                        <md-input v-model="courseCode"></md-input>
                    </md-input-container>
                    <md-input-container>
                        <label>Teaching Start: {{this.teachingStart}}</label>
                        <date-picker v-model="teachingStart"></date-picker>
                    </md-input-container>
                    <md-input-container>
                        <label>Teaching End: {{this.teachingEnd}}</label>
                        <date-picker v-model="teachingEnd"></date-picker>
                    </md-input-container>
                    <md-chips v-model="editableTopics"
                        md-input-placeholder="Course Topics">
                    </md-chips>
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
.md-fab {
    margin-left: auto;
}
</style>

<script lang="ts">
import DatePicker from "vue-flatpickr-component";
import { Vue, Component, Lifecycle } from "av-ts";
import { User, Course, CourseUser, Topic } from "../../interfaces/models";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";

import LeaderBoard from "../leaderboard/LeaderBoard.vue";
import TopicChip from "../util/TopicChip.vue";

const _MODAL_NAME = "course_create_modal";

@Component({
    components: {
        DatePicker,
        TopicChip,
        LeaderBoard
    }
})
export default class AdminView extends Vue {
    pTopics = [];
    courseCode = "";

    teachingStart: number | undefined = undefined;
    teachingEnd: number | undefined = undefined;

    pUser: User = undefined;
    pCourse: Course = undefined;
    networkError: string = "";

    updateUserCourse(courseUser: CourseUser) {
        this.pUser = courseUser.user;
        this.pCourse = courseUser.course;

        this.courseCode = this.pCourse.courseCode;

        if (this.pCourse.available === false) {
            this.openDialog();
        }

        if (this.pCourse.start) {
            this.teachingStart = this.pCourse.start;
        }
        if (this.pCourse.end) {
            this.teachingEnd = this.pCourse.end;
        }
    }

    get topics() {
        return this.pTopics;
    }
    get editableTopics() {
        return this.pTopics.map(x => x.name);
    }

    set editableTopics(newTopics: (Topic | string)[]) {
        const normalisedTopics: Topic[] = newTopics.map(x => {
            if (typeof x === "string") {
                return {
                    id: undefined,
                    name: x
                };
            }
            return x;
        });

        this.pTopics = normalisedTopics.reduce((carry: Topic[], topic: Topic) => {
            if (carry.find(x => topic.name.toLowerCase() === x.name.toLowerCase()) === undefined) {
                carry.push(topic);
            }
            return carry;
        }, []);
    }

    updateCourseTopics(topics: Topic[]) {
        this.pTopics = topics;
    }

    get course() {
        return this.pCourse;
    }
    get courseIsAvailable() {
        return this.course && this.course.available;
    }

    @Lifecycle
    created() {
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateUserCourse);
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateCourseTopics);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateUserCourse);
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateCourseTopics);
    }

    openDialog() {
        (this.$refs[_MODAL_NAME] as any).open();
    };

    localToUTC(date: string) {
        const [year, month, day] = date.split("-");

    }

    closeDialog() {
        UserService.updateCourse({
            courseCode: this.courseCode,
            courseName: this.pCourse.courseName,
            start: this.teachingStart,
            end: this.teachingEnd,
            available: true
        })
            .then(x => {
                if (x.error !== undefined) {
                    return this.networkError = x.error;
                }

                (this.$refs[_MODAL_NAME] as any).close();
            })
            .catch(err => {
                this.networkError = err;
            });
    };
}
</script>
