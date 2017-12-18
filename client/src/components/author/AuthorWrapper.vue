<template>
    <md-layout v-if="question" class="flex-vertical">
        <admin-buttons :canEdit="false"></admin-buttons>
        <author-view ref="authView" :question="question" :id="this.id"></author-view>
    </md-layout>
    <page-loader v-else :condition="!question"></page-loader>
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
import PageLoader from "../util/PageLoader.vue";
import { IQuestionBuilder, IQuestion } from "../../interfaces/models";
import AuthorView from "./AuthorView.vue";
import AdminButtons from "../util/AdminButtons.vue";
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

    pQuestion: IQuestionBuilder | undefined = undefined;

    updateQuestion() {
        QuestionService.getQuestionById(this.id)
            .then((question: IQuestion | undefined) => {
                if (question && question.canEdit !== undefined && !question.canEdit) {
                    this.$router.push(`/error/403`);
                }
                this.pQuestion = this.questionToBuilder(question);
            });
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
            topics: question.topics
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

    @Lifecycle
    created() {
        this.updateQuestion();
    }

    saveQuestion() {
        let aView: AuthorView = <AuthorView> this.$refs.authView;
        aView.validateUpload();
    }

    deleteQuestion() {
        QuestionService.deleteQuestion(this.id)
            .then(() => {
                addEventsToQueue([{
                    id: -7,
                    name: "Question Deleted",
                    description: "Successfully deleted question",
                    icon: "done"
                }]);
            })
            .then(() => {
                this.$router.go(-1);
            });
    }

}
</script>
