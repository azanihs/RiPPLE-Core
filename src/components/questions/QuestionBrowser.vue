<template>
    <div class="relative">
        <transition name="fade">
            <md-layout v-if="selectedQuestion"
                       key="1"
                       class="viewContainer">
                <md-layout md-flex="100"
                           class="questionContainer">
                    <question @userAnswer="setUserIsFinished"
                              @newQuestion="selectRandom"
                              class="question"
                              :question="selectedQuestion"></question>
                </md-layout>
            </md-layout>
        </transition>
        <md-layout :class="{hidden: selectedQuestion}"
                   key="2"
                   class="viewContainer">
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
.relative {
    position: relative;
    width: 100%;
}

.overview {
    margin-bottom: 2em;
}

.hidden {
    visibility: hidden;
    height: 0px;
    overflow: hidden;
}

.viewContainer {
    position: absolute;
    top: 8px;
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
import { Vue, Component, Lifecycle, Watch } from "av-ts";
import { Question as QuestionModel, Topic as TopicModel } from "../../interfaces/models";

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

    pTopics = [];

    questions: QuestionModel[] = [];
    searchedQuestions: QuestionModel[] = [];

    topicsToUse: TopicModel[] = [];

    selectedQuestion: QuestionModel = null;
    userIsFinished: boolean = false;

    @Lifecycle
    async created() {
        this.questions = await QuestionService.getRecommendedForUser(25);
    }

    get topics() {
        this.pTopics = TopicService.getAllAvailableTopics(topics => {
            this.pTopics = topics;
        });

        return this.pTopics;
    }

    get showQuestions() {
        return this.searchedQuestions.filter(x => x.topics.find(t => this.topicsToUse.indexOf(t) >= 0));
    }

    @Watch("selectedQuestion")
    questionChanged() {
        if (this.selectedQuestion != null) {
            window.scrollTo(0, 0);
        }
    }

    setUserIsFinished(newVal: boolean) {
        this.userIsFinished = newVal;
        this.selectedQuestion = null;
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

    generateCompetencies(itemsToInclude) {
        return UserService.userCompetencies(itemsToInclude);
    }

}
</script>
