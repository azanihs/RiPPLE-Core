<template>
    <md-layout>
        <md-layout class="headingContainer">
            <h1>Questions</h1>
            <question-search :availableQuestions="questions"
                             @searched="changeDisplay"></question-search>
        </md-layout>
        <md-layout md-gutter="16"
                   md-flex="100">
            <md-layout md-flex="33"
                       v-for="question in showQuestions"
                       :key="question.id">
                <question-preview class="questionCard"
                                  :data="question"></question-preview>
            </md-layout>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .headingContainer {
        border-bottom: 1px solid #222;
        margin: 8px;
    }
    
    .questionCard {
        min-width: 100%;
        margin-top: 8px;
        margin-bottom: 8px;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle } from "av-ts";
    import QuestionSearch from "./QuestionSearch.vue";
    import QuestionPreview from "./QuestionPreview.vue";

    import { Question } from "../../interfaces/models";
    import QuestionRepository from "../../repositories/QuestionRepository";

    @Component({
        components: {
            QuestionSearch,
            QuestionPreview
        }
    })
    export default class QuestionBrowser extends Vue {
        questions: Question[] = [];

        showQuestions: Question[] = [];

        @Lifecycle
        created() {
            this.questions = QuestionRepository.getMany(25);
        }

        changeDisplay(searchedQuestions: Question[]) {
            this.showQuestions = searchedQuestions;
        }
    }
</script>
