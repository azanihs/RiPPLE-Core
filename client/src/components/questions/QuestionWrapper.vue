<template>
    <md-layout v-if="question">
        <md-layout class="question-navigation">
            <admin-buttons v-if="canEdit" :id="id" :canEdit="canEdit"></admin-buttons>
            <action-buttons v-else>
                <md-button
                        slot="right"
                        class="md-warn"
                        @click="openDialog()">
                    <span>Report Question</span>
                    <md-icon>error_outline</md-icon>
                </md-button>
            </action-buttons>
        </md-layout>
        <question :question="question"></question>
    </md-layout>
    <page-loader v-else :condition="!question"></page-loader>
</template>

<style scoped>
.question-navigation {
    width: 100%;
    min-width: 100%;
    flex-direction: column;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";

import QuestionService from "../../services/QuestionService";
import PageLoader from "../util/PageLoader.vue";
import Question from "./Question.vue";
import { IQuestion } from "../../interfaces/models";
import ActionButtons from "../util/ActionButtons.vue";
import AdminButtons from "../util/AdminButtons.vue";

@Component({
    components: {
        Question,
        PageLoader,
        AdminButtons,
        ActionButtons
    }
})

export default class QuestionWrapper extends Vue {
    @Prop id = p<number>({
        required: true
    });

    canEdit: boolean = false;

    pQuestion: IQuestion | undefined = undefined;

    updateQuestion() {
        QuestionService.getQuestionById(this.id)
            .then((question: IQuestion | undefined) => {
                this.pQuestion = question;
                if (this.pQuestion && this.pQuestion.canEdit !== undefined && this.pQuestion.canEdit) {
                    this.canEdit = true;
                }
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
