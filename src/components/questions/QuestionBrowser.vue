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
        <div :class="{hidden: selectedQuestion}"
             key="2"
             class="viewContainer">
            <md-layout class="headingContainer"
                       md-flex="100">
                <variable-data-visualiser class="overview"
                                          @changeTopics="filterQuestionTopic"
                                          :dataCategories="topics"
                                          :compareList="generateCompetencies">
                </variable-data-visualiser>
                <question-search :page="page"
                                 :filterOut="topicsToFilter"
                                 @searched="changeDisplay">
                    <div class="md-table-card">
                        <md-table-pagination class="paginationControls"
                                             :md-total="totalQuestions"
                                             :md-size="25"
                                             :md-page="page"
                                             @pagination="nextPage">
                        </md-table-pagination>
                    </div>
                </question-search>
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

        </div>
    </div>
</template>

<style scoped>
.relative {
    position: relative;
    width: 100%;
}

.paginationControls {
    border-top: none !important;
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
    border-bottom: 1px solid #f2f2f2;
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
import Fetcher from "../../services/Fetcher";

import ActionButtons from "../util/ActionButtons.vue";
import QuestionSearch from "./QuestionSearch.vue";
import QuestionPreview from "./QuestionPreview.vue";
import Question from "./Question.vue";
import VariableDataVisualiser from "../charts/VariableDataVisualiser.vue";


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
    pData = {};
    pPage = 1;
    pQuestionCount = 0;

    searchedQuestions: QuestionModel[] = [];

    topicsToUse: TopicModel[] = [];

    selectedQuestion: QuestionModel = null;
    userIsFinished: boolean = false;

    updateTopics(topics) {
        this.pTopics = topics;
    };
    updateCompetencies(competency) {
        this.pData = competency;
    };

    @Lifecycle
    created() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateTopics);

        Fetcher.get(UserService.userCompetencies, {})
            .on(this.updateCompetencies);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateTopics);

        Fetcher.get(UserService.userCompetencies)
            .off(this.updateCompetencies);
    }

    get topics() {
        return this.pTopics;
    }

    get showQuestions() {
        return this.searchedQuestions;
        // Server handles topic filtering now.
        // return this.searchedQuestions.filter(x => x.topics.find(t => this.topicsToUse.indexOf(t) >= 0));
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

    changeDisplay(searchedQuestions) {
        this.pPage = searchedQuestions.page;
        this.searchedQuestions = searchedQuestions.questions;
        this.pQuestionCount = searchedQuestions.totalItems;
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

    get topicsToFilter() {
        return this.topics.filter(x => this.topicsToUse.indexOf(x) === -1).map(x => x.id);
    }

    generateCompetencies() {
        return UserService.userCompetencies;
    }

    get page() {
        return this.pPage;
    }

    get totalQuestions() {
        return this.pQuestionCount;
    }

    nextPage(pagination: { size: number, page: number }) {
        this.pPage = pagination.page;
    }

}
</script>
