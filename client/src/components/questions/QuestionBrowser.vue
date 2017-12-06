<template>
<md-layout md-gutter="8">
    <md-layout class="headingContainer"
        md-flex="100">
        <variable-data-visualiser class="overview"
            :dataCategories="topics"
            :compareList="generateCompetencies">
        </variable-data-visualiser>
        <question-search :page="page"
            :pageSize="pageSize"
            @searched="changeDisplay">
            <div class="md-table-card">
                <md-table-pagination class="paginationControls"
                    :md-total="totalQuestions"
                    md-label="Questions per page"
                    :md-size="pageSize"
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
            class="questionPreview">
            <router-link :to="'/question/id/' + question.id" class="questionLink">
                <question-preview class="questionCard"
                    :data="question"></question-preview>
            </router-link>
        </md-layout>
    </md-layout>
    <md-layout md-hide-large-and-up>
        <md-layout v-for="question in showQuestions"
            md-flex="100"
            :key="question.id"
            class="mobileQuestionPreview">
            <question-preview class="mobileQuestionCard"
                :data="question"></question-preview>
        </md-layout>
    </md-layout>
    <page-loader v-if="showQuestions.length == 0"></page-loader>
</md-layout>
</template>

<style scoped>
.questionLink {
    color: inherit !important;
}
.questionLink:hover {
    text-decoration: inherit !important;
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
import { Vue, Component, Lifecycle } from "av-ts";
import { Question as IQuestion, Topic as ITopic } from "../../interfaces/models";

import UserService from "../../services/UserService";
import TopicService from "../../services/TopicService";
import Fetcher from "../../services/Fetcher";

import ActionButtons from "../util/ActionButtons.vue";
import QuestionSearch from "./QuestionSearch.vue";
import QuestionPreview from "./QuestionPreview.vue";
import Question from "./Question.vue";
import VariableDataVisualiser from "../charts/VariableDataVisualiser.vue";
import PageLoader from "../util/PageLoader.vue";


@Component({
    components: {
        ActionButtons,
        VariableDataVisualiser,
        QuestionSearch,
        QuestionPreview,
        Question,
        PageLoader
    }
})
export default class QuestionBrowser extends Vue {

    pTopics: ITopic[] = [];

    pPage = 1;
    pPageSize = 25;
    pQuestionCount = 0;

    searchedQuestions: IQuestion[] = [];
    topicsToUse: ITopic[] = [];

    updateTopics(topics: ITopic[]) {
        this.pTopics = topics;
    };

    @Lifecycle
    created() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateTopics);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateTopics);
    }

    get topics() {
        return this.pTopics;
    }

    get showQuestions() {
        return this.searchedQuestions;
    }

    changeDisplay(searchedQuestions: { questions: IQuestion[], page: number, totalItems: number }) {
        this.pPage = searchedQuestions.page;
        this.searchedQuestions = searchedQuestions.questions;
        this.pQuestionCount = searchedQuestions.totalItems;
    }

    filterQuestionTopic(topicsToUse: ITopic[]) {
        this.topicsToUse = topicsToUse;
    }

    generateCompetencies() {
        return UserService.userCompetencies;
    }

    get page() {
        return this.pPage;
    }

    get pageSize() {
        return this.pPageSize;
    }

    get totalQuestions() {
        return this.pQuestionCount;
    }

    nextPage(pagination: { size: number, page: number }) {
        this.pPage = pagination.page;
        this.pPageSize = pagination.size;
    }

}
</script>
