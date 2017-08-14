<template>
    <div>
        <transition name="fade">
            <md-layout v-if="selectedQuestion"
                       key="1"
                       class="viewContainer">
                <!-- Header -->
                <action-buttons class=""
                                @back="selectedQuestion = null"
                                @randomQuestion="selectRandom"></action-buttons>
                <md-layout md-flex="100"
                           class="questionContainer">
                    <question @userAnswer="setUserIsFinished"
                              class="question"
                              :question="selectedQuestion"></question>
                </md-layout>
            </md-layout>
        </transition>
        <md-layout :class="{hidden: selectedQuestion}"
                   key="2"
                   class="viewContainer">
            <!-- Header -->
            <md-layout class="headingContainer"
                       md-flex="100">
                <variable-data-visualiser class="overview"
                                          @changeTopics="filterQuestionTopic"
                                          :dataCategories="topics"
                                          :compareList="generateCompetencies">
                </variable-data-visualiser>
                <question-search :availableQuestions="questions"
                                 @searched="changeDisplay"></question-search>
            </md-layout>
            <md-layout md-hide-xsmall
                       md-hide-small
                       md-hide-medium>
                <md-layout v-for="question in showQuestions"
                           md-flex="33"
                           md-gutter
                           :key="question.id"
                           class="questionPreview"
                           @click.native="openQuestionPreview(question)">
                    <question-preview class="questionCard"
                                      :data="question"></question-preview>
                </md-layout>
            </md-layout>
            <md-layout md-hide-large-and-up>
                <md-layout v-for="question in showQuestions"
                           md-flex="100"
                           :key="question.id"
                           class="mobileQuestionPreview"
                           @click.native="openQuestionPreview(question)">
                    <question-preview class="mobileQuestionCard"
                                      :data="question"></question-preview>
                </md-layout>
            </md-layout>
        </md-layout>
    </div>
</template>

<style scoped>
.overview {
    margin-bottom: 2em;
}

.hidden {
    visibility: hidden;
    height: 0px;
    overflow: hidden;
}

.viewContainer {
    position: relative;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity .3s ease;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}

.headingContainer {
    border-bottom: 1px solid #222;
    margin: 8px;
}

.questionPreview {
    padding: 8px;
}

.questionCard {
    min-width: 100%;
    margin-top: 8px;
    margin-bottom: 8px;
}

.mobileQuestionCard {
    margin: 8px;
    padding: 0px;
}

.question {
    width: 100%;
    flex-basis: 100%;
}

.questionContainer {
    margin-bottom: 2em;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { Question as QuestionModel } from "../../interfaces/models";

import UserService from "../../services/UserService";
import QuestionService from "../../services/QuestionService";
import TopicService from "../../services/TopicService";

import ActionButtons from "../util/ActionButtons.vue";
import VariableDataVisualiser from "../charts/VariableDataVisualiser.vue";
import QuestionSearch from "./QuestionSearch.vue";
import QuestionPreview from "./QuestionPreview.vue";
import Question from "./Question.vue";


@Component({
    components: {
        ActionButtons,
        VariableDataVisualiser,
        QuestionSearch,
        QuestionPreview,
        Question
    }
})
export default class QuestionBrowser extends Vue {
    questions: QuestionModel[] = QuestionService.getRecommendedForUser(25);

    searchedQuestions: QuestionModel[] = [];

    topicsToUse: string[] = [];

    selectedQuestion: QuestionModel = null;
    userIsFinished: boolean = false;

    setUserIsFinished(newVal: boolean) {
        this.userIsFinished = newVal;
    }

    get maxOverlayHeight() {
        return 7 * window.innerHeight / 8 + "px";
    }

    get showQuestions() {
        return this.searchedQuestions.filter(x => {
            return x.topics.find(t => this.topicsToUse.indexOf(t) >= 0);
        });
    }

    changeDisplay(searchedQuestions: QuestionModel[]) {
        this.searchedQuestions = searchedQuestions;
    }


    selectRandom() {
        this.selectedQuestion = null;
        Vue.nextTick(() => {
            this.selectedQuestion = this.showQuestions[Math.floor(Math.random() * this.showQuestions.length)];
        });
    }

    openQuestionPreview(question) {
        if (this.selectedQuestion == question) {
            this.selectedQuestion = null;
        } else {
            this.selectedQuestion = question;
        }
    }

    filterQuestionTopic(topicsToUse) {
        this.topicsToUse = topicsToUse;
    }

    get topics() {
        return TopicService.getAllAvailableTopics();
    }

    generateCompetencies(itemsToInclude) {
        return UserService.userCompetencies(itemsToInclude);
    }

}
</script>
