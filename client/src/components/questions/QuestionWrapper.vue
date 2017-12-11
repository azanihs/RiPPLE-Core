<template>
    <question v-if="question" :question="question"></question>
    <page-loader v-else :condition="!question"></page-loader>
</template>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";

import QuestionService from "../../services/QuestionService";
import PageLoader from "../util/PageLoader.vue";
import Question from "./Question.vue";
import { IQuestion } from "../../interfaces/models";

@Component({
    components: {
        Question,
        PageLoader
    }
})

export default class QuestionWrapper extends Vue {
    @Prop id = p<number>({
        required: true
    });

    pQuestion: IQuestion | undefined = undefined;

    updateQuestion() {
        QuestionService.getQuestionById(this.id)
            .then((question: IQuestion | undefined) => {
                this.pQuestion = question;
            });
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
