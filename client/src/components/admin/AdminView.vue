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
                <md-chips v-model="editableTopics"
                    @change="topicsEdited"
                    md-input-placeholder="Course Topics">
                </md-chips>
                <md-button class="md-fab md-primary"
                    @click="openDialog()">
                    <md-icon>save</md-icon>
                </md-button>
            </md-card>
        </md-layout>
        <leader-board class="componentSeparator"
            @userData="generateCSVString"
            v-if="courseIsAvailable"></leader-board>
        <md-layout v-if="courseIsAvailable"
            class="componentSeparator"
            md-flex="100">
            <md-card>
                <md-button @click="downloadCSVString" class="md-raised">Download Spreadsheet Results</md-button>
                <md-button class="md-raised">Download Database Dump</md-button>
            </md-card>
        </md-layout>
        <md-dialog ref="course_create_modal"
            :md-click-outside-to-close="false"
            :md-esc-to-close="false">
            <md-dialog-title>Create new course</md-dialog-title>
            <md-dialog-content>
                <p v-if="courseIsAvailable">Your course: {{courseCode}} does not appear to exist.</p>
                <p v-else>Updating course: {{courseCode}}</p>
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
                        @change="topicsEdited"
                        md-input-placeholder="Course Topics">
                    </md-chips>
                </form>
            </md-dialog-content>

            <md-dialog-actions>
                <md-button v-if="courseIsAvailable"
                    class="md-primary"
                    @click="closeDialog()">Close</md-button>
                <md-button class="md-primary"
                    @click="saveCourseInformation()">{{courseIsAvailable ? "Upadte" : "Create"}}</md-button>
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
import Papa from "papaparse";

import { Vue, Component, Lifecycle } from "av-ts";
import { UserSummary, User, Course, CourseUser, Topic } from "../../interfaces/models";

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

    teachingStart: string | undefined = undefined;
    teachingEnd: string | undefined = undefined;

    pUser: User = undefined;
    pCourse: Course = undefined;
    pCsvString: string = "";
    networkError: string = "";

    updateCourseUser(courseUser: CourseUser) {
        if (courseUser.roles.indexOf("Instructor") == -1) {
            this.$router.push("error/403");
        }

        this.pUser = courseUser.user;
        this.pCourse = courseUser.course;

        this.courseCode = this.pCourse.courseCode;

        if (this.pCourse.available === false) {
            this.openDialog();
        }

        if (this.pCourse.start) {
            this.teachingStart = this.serverToLocal(this.pCourse.start);
        }
        if (this.pCourse.end) {
            this.teachingEnd = this.serverToLocal(this.pCourse.end);
        }
    }

    get topics() {
        return this.pTopics;
    }

    get editableTopics() {
        return this.pTopics.map(x => x.name);
    }

    topicsEdited(newTopics: string[]) {
        this.editableTopics = newTopics;
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
            .on(this.updateCourseUser);
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateCourseTopics);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateCourseUser);
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateCourseTopics);
    }

    openDialog() {
        const modal = this.$refs[_MODAL_NAME] as any;
        if (modal) {
            requestAnimationFrame(() => modal.open());
        }
    };

    localToUTC(date?: string) {
        if (date === undefined) return undefined;

        const [year, month, day] = date.split("-");
        // Convert to UTC and from milliseconds to seconds
        return Date.UTC(+year, +month, +day) / 1000;
    }

    serverToLocal(UTCTimestamp: number) {
        const date = new Date(0);
        date.setUTCSeconds(UTCTimestamp);

        return date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
    }


    closeDialog() {
        (this.$refs[_MODAL_NAME] as any).close();
    }

    saveCourseInformation() {
        UserService.updateCourse({
            course: {
                courseCode: this.courseCode,
                courseName: this.pCourse.courseName,
                start: this.localToUTC(this.teachingStart),
                end: this.localToUTC(this.teachingEnd),
                available: true
            },
            topics: this.topics
        })
            .then(x => {
                if (x.error !== undefined) {
                    return this.networkError = x.error;
                }
                this.updateCourseUser(x);
                this.closeDialog();
            })
            .catch(err => {
                this.networkError = err;
            });
    };

    generateCSVString(userData: UserSummary[]) {
        this.pCsvString = Papa.unparse(userData, {
            quotes: true,
            quoteChar: `"`,
            delimiter: ",",
            header: true,
            newline: "\r\n"
        });
    }

    downloadCSVString(e: MouseEvent) {
        // Encode the CSV string as a URI
        const uri = encodeURI("data:text/csv;charset=utf-8," + this.pCsvString);
        // Create a mock anchor element and point it at the CSV URI
        const _a = document.createElement("a");
        _a.target = "_blank";
        _a.href = uri;
        _a.download = this.pCourse.courseCode + "_ripple_export_" + Date.now() + ".csv";
        _a.style.opacity = "0";

        // Add the anchor tag to the DOM and programmically click it
        document.body.appendChild(_a);
        _a.dispatchEvent(new MouseEvent("click", {
            bubbles: false
        }));

        // Remove the anchor element from the DOM after it has been clicked
        document.body.removeChild(_a);
    }
}
</script>
