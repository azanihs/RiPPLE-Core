<template>
    <md-layout v-if="!id || question" class="flex-vertical">
        <admin-buttons
            :showEdit="false"
            :id="id"
            :prevQuestions="prevQuestions"
            @saveQuestion="saveQuestion"
            @deleteQuestion="openDialog"
            @version="version"></admin-buttons>
        <author-view ref="authView"
            :version="pVersion"
            :question="question"
            :id="this.id"></author-view>
        <md-dialog ref="delete_modal">
            <md-dialog-title>Delete Question</md-dialog-title>
            <md-dialog-content>
                <p>Are you sure you want to delete?</p>
            </md-dialog-content>
            <md-dialog-actions>
                <md-button
                    @click="closeDialog()">Cancel</md-button>
                    <md-button class="md-warn"
                    @click="deleteQuestion()">Delete</md-button>
            </md-dialog-actions>
        </md-dialog>
    </md-layout>
    <page-loader v-else :condition="id && !question"></page-loader>
</template>

<style scoped>
.flex-vertical {
    display:flex;
    flex-direction: column;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";

import QuestionService from "../../services/QuestionService";
import Fetcher from "../../services/Fetcher";

import PageLoader from "../util/PageLoader.vue";
import { IQuestionBuilder, IQuestion } from "../../interfaces/models";
import AuthorView from "./AuthorView.vue";
import AdminButtons from "../util/AdminButtons.vue";
import { addEventsToQueue } from "../../util";
import { serverToLocal } from "../../util";

const _MODAL_NAME = "delete_modal";

@Component({
    components: {
        AuthorView,
        PageLoader,
        AdminButtons
    }
})

export default class AuthorWrapper extends Vue {
    @Prop id = p<number>({
        required: false
    });

    @Prop returnTo = p<string>({});

    pQuestion: IQuestionBuilder | undefined = undefined;
    pCurrent: IQuestionBuilder | undefined = undefined;
    prevQuestions: IQuestionBuilder[] = [];
    pVersion: number = 0;

    updateQuestion() {
        if (this.id) {
            QuestionService.getQuestionById(this.id)
                .then((question: IQuestion | undefined) => {
                    if (question && question.canEdit !== undefined && !question.canEdit) {
                        this.$router.push(`/error/403`);
                    }
                    this.pQuestion = this.questionToBuilder(question!);
                    this.pCurrent = this.questionToBuilder(question!);
                });

            QuestionService.getPreviousQuestions(this.id)
                .then((questionList: IQuestion[]) => {
                    this.prevQuestions = [];
                    questionList.forEach( question => {
                        this.prevQuestions.push(this.questionToBuilder(question)!);
                    });
                });
        }
    }

    questionToBuilder(question: IQuestion | undefined) {
        if (question === undefined) {
            return undefined;
        }
        let builder: IQuestionBuilder = {
            content: question.content,
            explanation: question.explanation,
            responses: {
                A: question.distractors[0].content,
                B: question.distractors[1].content,
                C: question.distractors[2].content,
                D: question.distractors[3].content
            },
            correctIndex: "A",
            topics: question.topics,
            createdAt: serverToLocal(question.createdAt!)
        };
        question.distractors.forEach(d => {
            if (d.isCorrect) {
                builder.correctIndex = d.response;
            }
        });
        return builder;
    }

    get question() {
        return this.pQuestion!;
    }

    set question(newQuestion: IQuestionBuilder) {
        this.pQuestion = newQuestion;
    }

    @Lifecycle
    created() {
        this.updateQuestion();
    }

    saveQuestion() {
        let aView: AuthorView = <AuthorView> this.$refs.authView;
        aView.validateUpload();
    }

    deleteQuestion() {
        if (this.id) {
            QuestionService.deleteQuestion(this.id)
                .then(() => {
                    addEventsToQueue([{
                        name: "Question Deleted",
                        description: "Successfully deleted question",
                        icon: "done"
                    }]);
                    QuestionService.getReportAggregates()
                        .then(x => {
                            Fetcher.get(QuestionService.getReportAggregates)
                                .update(x);
                        });
                })
                .then(() => {
                    this.closeDialog();
                    this.$router.push({ "name": this.returnTo });
                });
        }
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

    version(version: number) {
        this.pVersion = version;
        if (version == 0) {
            this.question = this.pCurrent!;
        } else {
            this.question = this.prevQuestions[version-1];
        }
    }

}
</script>
