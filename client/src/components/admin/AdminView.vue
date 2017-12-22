<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100">
            <md-card>
                <h2>Administration Page for: {{ pCourseCode }}</h2>
                <!-- <md-input-container>
                    <label>Teaching Start: {{ this.teachingStart }}</label>
                    <date-picker v-model="teachingStart"></date-picker>
                </md-input-container>
                <md-input-container>
                    <label>Teaching End: {{ this.teachingEnd }}</label>
                    <date-picker v-model="teachingEnd"></date-picker>
                </md-input-container> -->
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
            v-if="courseIsAvailable"></leader-board>
        <md-layout v-if="courseIsAvailable"
            class="componentSeparator"
            md-flex="100">
            <md-card>
                <md-button @click="downloadCSVString" class="md-raised">Download Full Spreadsheet Results</md-button>
                <md-button @click="downloadConsentedCSV" class="md-raised">Download Consented Spreadsheet Results</md-button>
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
                    <!-- <md-input-container>
                        <label>Teaching Start: {{this.teachingStart}}</label>
                        <date-picker v-model="teachingStart"></date-picker>
                    </md-input-container>
                    <md-input-container>
                        <label>Teaching End: {{this.teachingEnd}}</label>
                        <date-picker v-model="teachingEnd"></date-picker>
                    </md-input-container> -->
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
                    @click="saveCourseInformation()">{{courseIsAvailable ? "Update" : "Create"}}</md-button>
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
import { IUserSummary, IUser, ICourse, ICourseUser, ITopic } from "../../interfaces/models";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";
import { serverToLocal, localToUTC, isAdmin } from "../../util";

import LeaderBoard from "../leaderboard/LeaderBoard.vue";
import TopicChip from "../util/TopicChip.vue";

const _MODAL_NAME = "course_create_modal";

interface IConstructTopic {
    id?: number,
    name: string;
};

@Component({
    components: {
        DatePicker,
        TopicChip,
        LeaderBoard
    }
})
export default class AdminView extends Vue {
    pTopics: ITopic[] = [];
    pCourseCode = "";

    teachingStart: string | undefined = "0";
    teachingEnd: string | undefined = "0";

    pUser: IUser | undefined = undefined;
    pCourse: ICourse| undefined = undefined;
    pCsvString: string = "";
    networkError: string = "";

    updateCourseUser(courseUser: ICourseUser) {
        if (!isAdmin(courseUser.roles)) {
            this.$router.push("error/403");
        }

        this.pUser = courseUser.user;
        this.pCourse = courseUser.course;

        this.pCourseCode = this.pCourse.courseCode;

        if (this.pCourse.available === false) {
            this.openDialog();
        }

        if (this.pCourse.start) {
            this.teachingStart = serverToLocal(this.pCourse.start);
        }
        if (this.pCourse.end) {
            this.teachingEnd = serverToLocal(this.pCourse.end);
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

    set editableTopics(newTopics: (ITopic | string)[]) {
        const normalisedTopics: IConstructTopic[] = newTopics.map(x => {
            if (typeof x === "string") {
                return {
                    id: undefined,
                    name: x
                };
            }
            return x;
        });

        this.pTopics = normalisedTopics.reduce((carry: ITopic[], topic: IConstructTopic) => {
            if (carry.find(x => topic.name.toLowerCase() === x.name.toLowerCase()) === undefined) {
                carry.push(topic as ITopic);
            }
            return carry;
        }, []);
    }

    updateCourseTopics(topics: ITopic[]) {
        this.pTopics = topics;
    }

    get course() {
        return this.pCourse;
    }

    get courseCode() {
        return this.pCourseCode;
    }

    get courseIsAvailable() {
        return this.course && this.course.available;
    }

    @Lifecycle
    mounted() {
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

    closeDialog() {
        (this.$refs[_MODAL_NAME] as any).close();
    }

    saveCourseInformation() {
        if (this.pCourse == undefined) {
            return;
        }

        UserService.updateCourse({
            course: {
                courseCode: this.pCourseCode,
                courseName: this.pCourse.courseName,
                start: localToUTC(this.teachingStart),
                end: localToUTC(this.teachingEnd),
                available: true
            },
            topics: this.topics
        })
        .then((x: any | ICourseUser) => {
            if (x.error !== undefined) {
                this.networkError = x.error;
            } else {
                this.updateCourseUser(x);
                this.closeDialog();
            }
        });
    };

    downloadCSVString() {
        UserService.getUserStats().then( results =>
        this.downloadCSV(this.makeCSVString(results,
            ["id", "firstName", "lastName", "questionsAuthored", "questionsAnswered",
                "questionsAnsweredCorrectly", "achievementsEarned", "questionsRated"])!));
    }

    downloadConsentedCSV() {
        UserService.getConsentedUserStats().then(results =>
        this.downloadCSV(this.makeCSVString(results,
            ["rank", "questionsAuthored", "questionsAnswered",
                "questionsAnsweredCorrectly", "achievementsEarned", "questionsRated"])!));
    }

    makeCSVString(userData: IUserSummary[], fields: string[]) {
        if (userData.length == 0) {
            return;
        }

        const unparseData = {
            fields: fields,
            data: userData
        };
        return Papa.unparse(unparseData, {
            quotes: true,
            delimiter: ",",
            newline: "\r\n"
        });
    }

    downloadCSV(csvString: string) {
        // update CSV string headings
        csvString = this.updateHeadings(csvString);
        // Encode the CSV string as a URI
        const uri = encodeURI("data:text/csv;charset=utf-8," + csvString);
        // Create a mock anchor element and point it at the CSV URI
        const _a = document.createElement("a");
        _a.target = "_blank";
        _a.href = uri;
        _a.download = this.pCourseCode + "_ripple_export_" + Date.now() + ".csv";
        _a.style.opacity = "0";

        // Add the anchor tag to the DOM and programmatically click it
        document.body.appendChild(_a);
        _a.dispatchEvent(new MouseEvent("click", {
            bubbles: false
        }));

        // Remove the anchor element from the DOM after it has been clicked
        document.body.removeChild(_a);
    }

    updateHeadings(csvString:string) {
        let headings = [["id", "ID"],
            ["firstName", "First Name"],
            ["lastName", "Last Name"],
            ["rank", "Rank"],
            ["questionsAuthored", "Questions Authored"],
            ["questionsAnswered", "Questions Answered"],
            ["questionsAnsweredCorrectly", "Questions Answered Correctly"],
            ["achievementsEarned", "Achievements Earned"],
            ["questionsRated", "Questions Rated"]];

        let splitString = csvString.split(/\r\n|\r|\n/);
        let headerString = splitString[0];
        for (let i of headings) {
            headerString = headerString.replace(i[0], i[1]);
        }
        splitString[0] = headerString;
        csvString = splitString.join("\r\n");
        return csvString;
    }
}
</script>
