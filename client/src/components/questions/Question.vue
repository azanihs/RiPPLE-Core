<template>
    <md-layout :class="bottomSpaceClass">
        <md-layout md-flex="100" class="adminQuestionStyle">
            <md-layout md-flex="100"
                       class="questionContainer componentSeparator">
                <md-card>
                    <p class="questionContent"
                       v-html="question.content">
                    </p>
                    <question-details :question="question"></question-details>
                </md-card>
            </md-layout>
            <question-response class="responseContainer componentSeparator"
                               :question="question"
                               :preview="preview"
                               @userAnswer="updateUserAnswer">
                <md-layout md-flex="100"
                           v-if="userIsFinishedWithQuestion && !preview">
                    <md-layout class="between"
                               md-hide-xsmall
                               md-hide-small>
                        <question-rater class="rater"
                                        icon="start">Rate Quality</question-rater>
                        <question-rater class="rater"
                                        icon="school">Rate Difficulty</question-rater>
                    </md-layout>
                    <md-layout class="between small"
                               md-hide-small-and-up>
                        <question-rater class="rater"
                                        icon="start">Rate Quality</question-rater>
                        <question-rater class="rater"
                                        icon="school">Rate Difficulty</question-rater>
                    </md-layout>
                </md-layout>
            </question-response>
        </md-layout>
        <md-speed-dial v-if="showSpeedDial"
                       md-open="hover"
                       md-direction="left"
                       class="md-fab-bottom-right floatingAction">
            <md-button class="md-fab md-primary"
                       @click="nextQuestion"
                       md-fab-trigger>
                <md-icon md-icon-morph>arrow_forward</md-icon>
                    <md-icon>arrow_forward</md-icon>
                    <md-tooltip md-direction="top">Next Question</md-tooltip>
            </md-button>

            <md-button class="md-fab md-primary md-mini md-clean"
                       @click="closeQuestion">
                <md-icon>keyboard_return</md-icon>
                <md-tooltip md-direction="top">Return</md-tooltip>
            </md-button>
            <md-button class="md-fab md-primary md-mini md-clean"
                            @click="openDialog">
                <md-icon>error_outline</md-icon>
                <md-tooltip md-direction="top">Report Question</md-tooltip>
            </md-button>
        </md-speed-dial>
        <md-dialog ref="report_question_modal"
            :md-click-outside-to-close="true"
            :md-esc-to-close="true">
            <md-dialog-title>Report Question</md-dialog-title>
            <md-dialog-content>
                <form>
                    <label>Report question for:</label><br>
                    <topic-chip class="topicChip" v-for="reason in pReasonList"
                        :key="reason"
                        :disabled="!reasonIsUsed(reason)"
                        @click.native="toggleReason(reason)">
                        {{reason}}
                    </topic-chip>
                    <md-input-container>
                        <label>Add an explanation:</label>
                        <md-textarea v-model="reason"></md-textarea>
                    </md-input-container>
                    <div class="right">
                        <md-button class="md-fab md-primary md-mini md-clean"
                                @click="closeDialog()">
                            <md-icon>clear</md-icon>
                            <md-tooltip md-direction="top">Cancel</md-tooltip>
                        </md-button>
                        <md-button class="md-fab md-primary md-mini md-clean"
                                @click="reportQuestion()">
                            <md-icon>done</md-icon>
                            <md-tooltip md-direction="top">Report Question</md-tooltip>
                        </md-button>
                    </div>
                </form>
            </md-dialog-content>
        </md-dialog>
    </md-layout>
</template>

<style>
.questionContent {
    width: 100%;
}

.questionContent img {
    /* Also used in questionResponse.vue */
    border: 1px solid #bbb;
    box-shadow: 2px 2px 5px #aaa;
}
</style>

<style scoped>
.fade-enter-active {
    transition: opacity 250ms ease;
}

.fade-enter {
    opacity: 0;
}
h2 {
    width: 100%;
}

.questionContent {
    margin-top: 0px;
}

.questionContainer,
.responseContainer {
    min-width: 100%;
    flex: 0 1 100%;
}

.rater {
    min-width: 40%;
    max-width: 45%;
    width: 40%;
    margin-top: 1em;
}

.rater:nth-child(even) {
    text-align: right;
    flex-direction: row-reverse;
}

.between {
    margin-top: 2em;
    border-top: 1px solid #eee;
    justify-content: space-between;
}

.between.small .rater {
    min-width: 100%;
    width: 100%;
    text-align: left;
    flex-direction: row;
}

.floatingAction {
    position: fixed !important;
    bottom: 16px !important;
    right: 16px !important;
}

.floatingAction > button {
    background-color: #1d323a !important;
}

.bottomSpace {
    margin-bottom: 4em;
}

.topicChip {
    margin-top:0.5em;
}

.right {
    text-align:right;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import { IQuestion } from "../../interfaces/models";

import { addEventsToQueue } from "../../util";
import QuestionService from "../../services/QuestionService";

import QuestionRater from "./QuestionRater.vue";
import QuestionDetails from "./QuestionDetails.vue";
import QuestionResponse from "./QuestionResponse.vue";
import Fetcher from "../../services/Fetcher";


import TopicChip from "../util/TopicChip.vue";

const _MODAL_NAME = "report_question_modal";

@Component({
    components: {
        QuestionRater,
        QuestionResponse,
        QuestionDetails,
        TopicChip
    }
})
export default class Question extends Vue {
    @Prop question = p<IQuestion>({
        required: true
    });

    @Prop showSpeedDial = p<boolean>({
        default: true
    });

    @Prop showNavBar = p<boolean>({
        default: true
    });

    @Prop preview = p<boolean>({
        default: false
    });

    reason = "";
    pReasonList: string[] | undefined = undefined;
    reasonsUsed: string[] = [];
    networkMessage = "";

    userIsFinishedWithQuestion: boolean = false;

    updateUserAnswer(wasCorrect: boolean) {
        this.userIsFinishedWithQuestion = wasCorrect;
        if (this.question !== undefined && this.userIsFinishedWithQuestion) {
            this.question.responseCount++;
        }
    }

    get reasonList() {
        return this.pReasonList;
    }

    set reasonList(newList) {
        this.pReasonList = newList;
    }

    nextQuestion() {
        QuestionService.getNextRecommendedQuestion()
            .then(questionId => {
                if (questionId == this.question.id) {
                    addEventsToQueue([{
                        name: "Server Question Response",
                        description: "You may have no more recommended questions",
                        icon: "error"
                    }]);
                } else {
                    this.$router.push({
                        path: `/question/id/${questionId}`
                    });
                }
            });
    }

    closeQuestion() {
        this.$router.push("/question/answer");
    }

    reportQuestion() {
        if (this.reason.length > 0) {
            this.reasonsUsed.push(this.reason);
        }
        if (this.reasonsUsed.length == 0) {
            addEventsToQueue([{
                name: "Not enough reasons",
                description: "You must provide at least one reason.",
                icon: "error"
            }]);
            return;
        }
        QuestionService.reportQuestion(this.question.id, this.reasonsUsed)
            .then(_ => {
                addEventsToQueue([{
                    name: "Question Reported",
                    description: "Question Reported.",
                    icon: "done"
                }]);
                this.reasonsUsed.splice(0, this.reasonsUsed.length);
                this.reason = "";

                this.closeDialog();
            });
    }

    openDialog() {
        const modal = this.$refs[_MODAL_NAME] as any;
        if (modal) {
            requestAnimationFrame(() => modal.open());
        }
    }

    closeDialog() {
        (this.$refs[_MODAL_NAME] as any).close();
    }

    toggleReason(reasonToToggle: string) {
        const reasonIndex = this.reasonsUsed.indexOf(reasonToToggle);
        if (reasonIndex == -1) {
            this.reasonsUsed.push(reasonToToggle);
        } else {
            this.reasonsUsed.splice(reasonIndex, 1);
        }
    }

    reasonIsUsed(reason: string) {
        return this.reasonsUsed.indexOf(reason) >= 0;
    }

    updateReportReasons(reasons: string[]) {
        this.pReasonList = reasons;
    }

    @Lifecycle
    created() {
        Fetcher.get(QuestionService.getReportReasons)
            .on(this.updateReportReasons);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(QuestionService.getReportReasons)
            .off(this.updateReportReasons);
    }

    get bottomSpaceClass(): string {
        if (this.showSpeedDial) {
            return "bottomSpace";
        } else {
            return "";
        }
    }
}
</script>
