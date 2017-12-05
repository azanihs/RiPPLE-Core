<template>
    <md-layout class="bottomSpace">
        <md-layout md-hide-xsmall
                   md-hide-small
                   md-hide-medium
                   class="questionNavigation">
            <action-buttons @back="closeQuestion()" 
                    @report="openDialog()"></action-buttons>
        </md-layout>
        <md-layout md-flex="100">
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
                               @userAnswer="updateUserAnswer">
                <md-layout md-flex="100"
                           v-if="userIsFinishedWithQuestion">
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
                       class="md-fab-bottom-right floatingAction">
            <md-button class="md-fab md-primary"
                       @click="nextQuestion"
                       md-fab-trigger>
                <md-icon md-icon-morph>arrow_forward</md-icon>
                <md-icon v-if="!userIsFinishedWithQuestion">replay</md-icon>
                <md-tooltip v-if="!userIsFinishedWithQuestion"
                            md-direction="left">Skip Question</md-tooltip>

                <md-icon v-if="userIsFinishedWithQuestion">arrow_forward</md-icon>
                <md-tooltip v-if="userIsFinishedWithQuestion"
                            md-direction="left">Next Question</md-tooltip>
            </md-button>

            <md-button class="md-fab md-primary md-mini md-clean"
                       @click="closeQuestion">
                <md-icon>keyboard_return</md-icon>
                <md-tooltip md-direction="left">Return</md-tooltip>
            </md-button>
            <md-button class="md-fab md-primary md-mini md-clean"
                            @click="openDialog">
                <md-icon>error_outline</md-icon>
                <md-tooltip md-direction="left">Report Question</md-tooltip>
            </md-button>
        </md-speed-dial>
        <md-dialog ref="report_question_modal"
            :md-click-outside-to-close="true"
            :md-esc-to-close="true">
            <md-dialog-title>Report Question</md-dialog-title>
            <md-dialog-content>
                <form>
                    <label>Report question for:</label><br>
                    <topic-chip class="topicChip" v-for="reason in reasonList"
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
        <md-snackbar md-position="bottom center"
            ref="snackbar"
            md-duration="4000">
            <span>{{networkMessage}}</span>
            <md-button class="md-accent"
                @click="$refs.snackbar.close()">Close</md-button>
        </md-snackbar>
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
.questionNavigation {
    width: 100%;
    min-width: 100%;
}

.fade-enter-active {
    transition: opacity 250ms ease;
}

.fade-enter {
    opacity: 0;
}

.reportButton {
    margin-left: auto;
    margin-right: 0px;
    margin-top: 1em;
    margin-bottom: 1em;
    border: 1px solid #eee;
    width: 100%;
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

.actionContainer {
    justify-content: flex-end;
}

.actionButtons {
    flex: none !important;
}

.actionButtons .button {
    margin-top: auto;
    margin-bottom: auto;
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
import { Vue, Component, Prop, p } from "av-ts";
import { Question as QuestionModel } from "../../interfaces/models";

import QuestionService from "../../services/QuestionService";

import ActionButtons from "../util/ActionButtons.vue";
import QuestionRater from "./QuestionRater.vue";
import QuestionDetails from "./QuestionDetails.vue";
import QuestionResponse from "./QuestionResponse.vue";

import TopicChip from "../util/TopicChip.vue";

const _MODAL_NAME = "report_question_modal";

@Component({
    components: {
        ActionButtons,
        QuestionRater,
        QuestionResponse,
        QuestionDetails,
        TopicChip
    }
})
export default class Question extends Vue {
    @Prop question = p<QuestionModel>({
        required: true
    });

    @Prop showSpeedDial = p<boolean>({
        default: true
    });

    reason = "";
    reasonList = ["Inappropriate Content", "Incorrect Answer", "Incorrect Tags"];
    reasonsUsed: string[] = []
    networkMessage = "";

    userIsFinishedWithQuestion: boolean = false;

    updateUserAnswer(wasCorrect: boolean) {
        this.userIsFinishedWithQuestion = wasCorrect;

        // TODO: Emit an event rather than mutate own prop.
        this.question.responseCount++;
    }

    nextQuestion() {
        this.$emit("newQuestion");
    }

    closeQuestion() {
        this.$emit("userAnswer");
    }

    reportQuestion() {
        this.reasonsUsed.push(this.reason);
        QuestionService.reportQuestion(this.question, this.reasonsUsed.toString())
            .then(x => {
                if (x.error !== undefined) {
                    this.networkMessage = "Error Submitting Report.";
                    (this.$refs.snackbar as any).open();
                }
                this.networkMessage = "Question Reported.";
                (this.$refs.snackbar as any).open();
                this.closeDialog();
            })
            .catch(err => {
                this.networkMessage = err;
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
}
</script>
