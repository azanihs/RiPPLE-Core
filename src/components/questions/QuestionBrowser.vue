<template>
    <md-layout class="viewContainer">
        <md-layout class="headingContainer"
                   md-flex="100">
            <h1>Questions</h1>
            <question-search :availableQuestions="questions"
                             @searched="changeDisplay"></question-search>
        </md-layout>
        <md-layout :md-gutter="this.selectedQuestion ? 0 : 16"
                   :md-flex="this.selectedQuestion ? 25 : 100">
            <md-layout v-for="question in showQuestions"
                       :key="question.id"
                       class="questionPreview"
                       :class="{selected: question == selectedQuestion,}"
                       @click.native="openQuestionPreview(question)">
                <question-preview class="questionCard"
                                  :data="question"></question-preview>
            </md-layout>
        </md-layout>
        <div v-if="selectedQuestion"
             class="questionContainer">
            <question class="question"
                      ref="question"
                      :question="selectedQuestion"></question>
        </div>
    </md-layout>
</template>

<style scoped>
    .viewContainer {
        position: relative;
    }
    
    .questionOverlay {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0px;
        left: 0px;
        background-color: rgba(0, 0, 0, 0.2);
        border: 1px solid #ddd;
        z-index: 100;
    }
    
    .questionOverlayContainer {
        background-color: #fff;
        width: 90%;
        overflow: scroll;
        margin: auto;
    
        padding: 1em;
        position: relative;
        top: 50px;
        transition: top 10ms ease;
    }
    
    .headingContainer {
        border-bottom: 1px solid #222;
        margin: 8px;
    }
    
    .questionCard {
        min-width: 100%;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    
    .md-flex-25 .questionPreview {
        min-width: 100%;
    }
    
    .questionPreview {
        min-width: 33%;
    }
    
    .questionPreview.selected {
        min-width: 100%;
    }
    
    .question {
        margin-top: 8px;
        position: relative;
        top: 0px;
    }
    
    .questionContainer {
        margin-left: 2.5%;
        min-width: 72.5%;
        flex: 0 1 72.5%;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle } from "av-ts";
    import QuestionSearch from "./QuestionSearch.vue";
    import QuestionPreview from "./QuestionPreview.vue";
    import Question from "./Question.vue";

    import { Question as QuestionModel } from "../../interfaces/models";
    import QuestionRepository from "../../repositories/QuestionRepository";

    @Component({
        components: {
            QuestionSearch,
            QuestionPreview,
            Question
        }
    })
    export default class QuestionBrowser extends Vue {
        questions: QuestionModel[] = [];

        showQuestions: QuestionModel[] = [];

        selectedQuestion: QuestionModel = null;

        @Lifecycle
        created() {
            this.questions = QuestionRepository.getMany(25);
            window.addEventListener("scroll", this.scrolled);
        }

        @Lifecycle
        destroyed() {
            window.removeEventListener("scroll", this.scrolled);
        }


        get maxOverlayHeight() {
            return 7 * window.innerHeight / 8 + "px";
        }

        changeDisplay(searchedQuestions: QuestionModel[]) {
            this.showQuestions = searchedQuestions;
        }

        openQuestionPreview(question) {
            if (this.selectedQuestion == question) {
                this.selectedQuestion = null;
            } else {
                this.selectedQuestion = question;
            }
        }

        scrolled(e: Event) {
            if (this.$refs["question"]) {
                const questionComponent = this.$refs["question"] as Vue;
                const questionElement = questionComponent.$el as HTMLElement;
                const doc = document.documentElement;
                const top = (window.pageYOffset || doc.scrollTop) - (doc.clientTop || 0);
                //questionElement.style.top = top + "px";
            }
        }
    }
</script>
