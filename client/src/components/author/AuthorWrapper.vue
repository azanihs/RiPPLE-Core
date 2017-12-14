<template>
    <author-view v-if="question" :question="question"></author-view>
    <page-loader v-else :condition="!question"></page-loader>
</template>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";

import QuestionService from "../../services/QuestionService";
import PageLoader from "../util/PageLoader.vue";
import { IQuestionBuilder, IQuestion } from "../../interfaces/models";
import AuthorView from "./AuthorView.vue";

@Component({
    components: {
        AuthorView,
        PageLoader
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


}
</script>
