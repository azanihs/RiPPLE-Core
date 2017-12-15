<template>
    <md-layout v-if="question" class="question-navigation">
        <admin-buttons :id="id"
        :canSave="canSave"
        :prevQuestions="prevQuestions"
        @saveQuestion="saveQuestion"
        @version="version"></admin-buttons>
        <author-view ref="authView" :question="question" :id="this.id"></author-view>
        <div> {{ prevQuestions }} </div>
    </md-layout>
    <page-loader v-else :condition="!question"></page-loader>
</template>

<style scoped>
.question-navigation {
    width: 100%;
    min-width: 100%;
    flex-direction: column;
    flex: inherit;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";

import QuestionService from "../../services/QuestionService";
import PageLoader from "../util/PageLoader.vue";
import { IQuestionBuilder, IQuestion } from "../../interfaces/models";
import AuthorView from "./AuthorView.vue";
import AdminButtons from "../util/AdminButtons.vue";
import { serverToLocal } from "../../util";
import { addEventsToQueue } from "../../util";

@Component({
    components: {
        AuthorView,
        PageLoader,
        AdminButtons
    }
})

export default class AuthorWrapper extends Vue {
    @Prop id = p<number>({
        required: true
    });

    canSave: boolean = false;
    pQuestion: IQuestionBuilder | undefined = undefined;
    pCurrent: IQuestionBuilder;
    prevQuestions: IQuestionBuilder[] = [];

    updateQuestion() {
        QuestionService.getQuestionById(this.id)
            .then((question: IQuestion | undefined) => {
                if (question && question.canEdit !== undefined && !question.canEdit) {
                    this.$router.push(`/error/403`);
                }
                if (question === undefined) {
                    addEventsToQueue([{
                        id: -9,
                        name: "Error",
                        description: "Question does not exist",
                        icon: "error"
                    }]);
                    this.$router.go(-1);
                }
                this.pQuestion = this.questionToBuilder(<IQuestion>question);
                this.pCurrent = this.questionToBuilder(<IQuestion>question);
                this.canSave = true;
            });
        QuestionService.getPreviousQuestions(this.id)
            .then((questionList: IQuestion[]) => {
                this.prevQuestions = [];
                questionList.forEach( question => {
                    this.prevQuestions.push(this.questionToBuilder(question));
                });
            });
    }

    questionToBuilder(question: IQuestion) {
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
            createdAt: serverToLocal(question.createdAt)
        };
        question.distractors.forEach(d => {
            if (d.isCorrect) {
                builder.correctIndex = d.response;
            }
        });
        return builder;
    }

    get question() {
        return this.pQuestion;
    }

    set question(newQuestion: IQuestionBuilder | undefined) {
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

    version(version: number) {
        if (version == 0) {
            this.question = this.pCurrent;
        } else {
            this.question = this.prevQuestions[version-1];
        }
    }

}
</script>
