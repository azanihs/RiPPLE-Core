<template>
    <md-layout>
        <md-card md-flex="100" class="column">
            <h2>Reported Questions for: {{ pCourseCode }}</h2>
            <md-list>
                <md-list-item :disabled="true" class="md-expand-multiple hide-arrow" style="border-bottom:3px solid black">
                    <span>
                        Question ID
                    </span>
                    <span>
                        Total Reports
                    </span>
                    <span>
                        Last Report
                    </span>
                    <span>
                        Edit
                    </span>
                    <md-list-expand>
                        <md-list>
                            <md-list-item class="md-inset"> 1 </md-list-item>
                        </md-list>
                    </md-list-expand>
                </md-list-item>
                <md-list-item v-for="i in numReports"
                    class="md-expand-multiple row tableRow"
                    :key="i">
                    <span>
                        {{ reportAggregates[i-1]["questionID"] }}
                    </span>
                    <span>
                        {{ reportAggregates[i-1]['totalReports'] }}
                    </span>
                    <span>
                        {{ reportAggregates[i-1]['lastReport'] }}
                    </span>
                    <span>
                        <md-button class="md-primary md-raised"
                        @click="editQuestion(reportAggregates[i-1]['questionID'])">
                        Edit</md-button>
                    </span>
                    <md-list-expand>
                        <md-card style="">
                            <md-list style="width:80%;margin:auto">
                                <md-list-item :disabled="true" style="border-bottom:1px solid black">
                                    <span>
                                        Reported By
                                    </span>
                                    <span>
                                        Date
                                    </span>
                                    <span>
                                        Report Reason
                                    </span>
                                </md-list-item>
                                <md-list-item v-for="j in reports[i-1].length"
                                :key="j"
                                @click="openDialog(i-1, j-1)">
                                    <span>
                                        {{ reports[i-1][j-1]["author"] }}
                                    </span>
                                    <span>
                                        {{ reports[i-1][j-1]["createdAt"] }}
                                    </span>
                                    <span>
                                        {{ getShortReason(reports[i-1][j-1]["reason"]) }}
                                    </span>
                                </md-list-item>
                            </md-list>
                        </md-card>
                    </md-list-expand>
                </md-list-item>
            </md-list>
        </md-card>
        <md-dialog ref="report_modal"
            :md-click-outside-to-close="true"
            :md-esc-to-close="true">
            <md-dialog-title>Question Report</md-dialog-title>
            <md-dialog-content>
                <h3>Reported By:</h3>
                <p>{{ modalAuthor }}</p><br>
                <h3>Date:</h3>
                <p>{{ modalDate }}</p><br>
                <h3>Reason:</h3>
                <p>{{ modalReason }}</p>
            </md-dialog-content>
            <md-dialog-actions>
                <md-button class="md-primary"
                    @click="closeDialog()">Close</md-button>
            </md-dialog-actions>
        </md-dialog>
    </md-layout>
</template>

<style scoped>
.table {
    margin-top: 1em;
    flex-direction: column !important;
}

.column {
     flex-direction: column;
}

span {
    flex-grow: 1;
    flex-basis: 0;
    text-align: center;
}

.md-list-item:nth-child(even){
    background-color: #fafafa
}
.md-list-item:hover{
    background-color: #fafafa
}

.hide-arrow >>> i {
    opacity: 0;
}

</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";
import QuestionService from "../../services/QuestionService";
import { serverToLocal } from "../../util";

import { ICourseUser, IReport, IReportAggregate, IServerReportFull,
    IServerReport, IServerReportAggregate } from "../../interfaces/models";

const _MODAL_NAME = "report_modal";

@Component()
export default class ReportedQuestions extends Vue {
    itemsPerPage = 10;
    pageIndex = 1;
    pCourseCode: string = "";
    pReports: IReport[][] = [];
    reportAggregates: IReportAggregate[] = [];
    pNumReports: number = 0;
    pModalAuthor: string = "";
    pModalDate: string = "";
    pModalReason: string = "";

    get modalAuthor() {
        return this.pModalAuthor;
    }

    set modalAuthor(newAuth: string) {
        this.pModalAuthor = newAuth;
    }
    get modalDate() {
        return this.pModalDate;
    }

    set modalDate(newDate: string) {
        this.pModalDate = newDate;
    }
    get modalReason() {
        return this.pModalReason;
    }

    set modalReason(newReason: string) {
        this.pModalReason = newReason;
    }

    get reports() {
        return this.pReports;
    }

    set reports(newReports: IReport[][]) {
        this.pReports = newReports;
    }

    get numReports() {
        return this.pNumReports;
    }

    set numReports(newNum: number) {
        this.pNumReports = newNum;
    }

    updateReports(serverReport: IServerReportFull) {
        let reportList: IReport[][] = [];
        for (let i = 1; i < serverReport.reports.length; i++) {
            reportList.push([]);
            let report: IServerReport[] = <IServerReport[]>serverReport.reports[i];
            report.forEach(rep => {
                let reasons: string = "";
                rep.reasons.forEach(reason => {
                    reasons += reason.reasonText + ". ";
                });
                reasons = reasons.trim();
                let newRep: IReport = {
                    createdAt: serverToLocal(rep.createdAt),
                    author: rep.author,
                    reason: reasons
                };
                reportList[i-1].push(newRep);
            });
        }
        this.reports = reportList;
    };

    updateCourseUser(courseUser: ICourseUser) {
        if (courseUser.roles.indexOf("Instructor") == -1) {
            this.$router.push("error/403");
        }
        this.pCourseCode = courseUser.course.courseCode;
    }

    updateReportAggregates(serverReport: IServerReportFull) {
        this.reportAggregates = [];
        let aggregateList: IServerReportAggregate[] = <IServerReportAggregate[]>serverReport.reports[0];
        aggregateList.forEach(agg => {
            let newAgg: IReportAggregate = {
                questionID: agg.questionID,
                totalReports: agg.totalReports,
                lastReport: serverToLocal(agg.lastReport)
            };
            this.reportAggregates.push(newAgg);
        });
        this.pNumReports = this.reportAggregates.length;
    }

    getShortReason(reason: String) {
        if (reason.length > 20) {
            return reason.substring(0, 20) + "...";
        }
        return reason;
    }

    openDialog(i: number, j:any) {
        this.modalAuthor = this.reports[i][j]["author"];
        this.modalDate = this.reports[i][j]["createdAt"];
        this.modalReason = this.reports[i][j]["reason"];
        const modal = this.$refs[_MODAL_NAME] as any;
        if (modal) {
            requestAnimationFrame(() => modal.open());
        }
    };

    closeDialog() {
        (this.$refs[_MODAL_NAME] as any).close();
    }

    editQuestion(id: number) {
        this.$router.push({ path: `/question/edit/${id}` });
    }

    @Lifecycle
    created() {
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateCourseUser);
        Fetcher.get(QuestionService.getReportAggregates)
            .on(this.updateReportAggregates);
        Fetcher.get(QuestionService.getReportAggregates)
            .on(this.updateReports);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateCourseUser);
        Fetcher.get(QuestionService.getReportAggregates)
            .off(this.updateReportAggregates);
        Fetcher.get(QuestionService.getReportAggregates)
            .off(this.updateReports);
    }
}
</script>
