<template>
    <md-layout>
        <h2>Answer Question</h2>
        <!--<action-buttons @back="updateUserAnswer(true)"></action-buttons>-->
        <md-layout md-flex="100">
            <md-layout md-flex="50"
                       class="questionContainer">
                <md-card>
                    <p class="questionContent">
                        <img v-if="question.images.length > 0"
                             :src="question.images[0]"></img>
                        {{question.content}}
                    </p>
                    <question-details :question="question"></question-details>
                </md-card>
    
                <transition name="fade">
                    <md-layout md-flex="100"
                               v-if="userIsFinishedWithQuestion">
                        <md-layout class="between">
                            <question-rater class="rater"
                                            icon="start">Rate Quality</question-rater>
                            <question-rater class="rater"
                                            icon="school">Rate Difficulty</question-rater>
                        </md-layout>
                    </md-layout>
                </transition>
            </md-layout>
            <question-response class="responseContainer"
                               :question="question"
                               @userAnswer="updateUserAnswer"></question-response>
        </md-layout>
        <md-speed-dial md-open="hover"
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
                <md-icon>replay</md-icon>
                <md-tooltip md-direction="left">Return</md-tooltip>
            </md-button>
            <md-button class="md-fab md-primary md-mini md-clean">
                <md-icon>error_outline</md-icon>
                <md-tooltip md-direction="left">Report Question</md-tooltip>
            </md-button>
        </md-speed-dial>
    </md-layout>
</template>

<style scoped>
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

img {
    width: 50%;
    height: auto;
    float: left;
    border: 1px solid #bbb;
    margin-right: 10px;
    box-shadow: 2px 2px 5px #aaa;
}

h2 {
    width: 100%;
}

.questionContent {
    margin-top: 0px;
}

.questionContainer,
.responseContainer {
    min-width: 49.25%;
    flex: 0 1 49.25%;
    align-content: flex-start;
    align-items: flex-start;
}

.responseContainer {
    margin-left: 1.5%;
}

.rater {
    min-width: 100%;
}

.rater {
    margin-top: 1em;
}

.between {
    justify-content: space-between;
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

.floatingAction>button {
    background-color: #1d323a !important;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import { Question as QuestionModel } from "../../interfaces/models";

import QuestionRater from "./QuestionRater.vue";
import ActionButtons from "../util/ActionButtons.vue";
import QuestionDetails from "./QuestionDetails.vue";
import QuestionResponse from "./QuestionResponse.vue";
import QuestionService from "../../services/QuestionService";

@Component({
    components: {
        ActionButtons,
        QuestionRater,
        QuestionResponse,
        QuestionDetails
    }
})
export default class Question extends Vue {
    @Prop question = p({
        required: true
    }) as QuestionModel;

    userIsFinishedWithQuestion: boolean = false;

    updateUserAnswer(n: boolean) {
        this.userIsFinishedWithQuestion = n;
    }

    nextQuestion() {
        this.$emit("newQuestion");
    }

    closeQuestion() {
        this.$emit("userAnswer");
    }
}
</script>
