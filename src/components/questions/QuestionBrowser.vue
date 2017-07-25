<template>
    <div>
        <transition name="fade">
            <md-layout v-if="selectedQuestion"
                       key="1"
                       class="viewContainer">
                <!-- Header -->
                <action-buttons @back="selectedQuestion = null"></action-buttons>
    
                <md-layout class="questionContainer">
                    <question @userAnswer="() => userIsFinished = true"
                              class="question"
                              ref="question"
                              :question="selectedQuestion"></question>
                    <action-buttons @back="selectedQuestion = null"></action-buttons>
                </md-layout>
            </md-layout>
        </transition>
        <md-layout :class="{hidden: selectedQuestion}"
                   key="2"
                   class="viewContainer">
            <!-- Header -->
            <md-layout class="headingContainer"
                       md-flex="100">
                <h1>Questions</h1>
                <question-search :availableQuestions="questions"
                                 @searched="changeDisplay"></question-search>
            </md-layout>
            <md-layout md-gutter="16">
                <md-layout v-for="question in showQuestions"
                           md-gutter
                           :key="question.id"
                           class="questionPreview"
                           :class="{selected: question == selectedQuestion,}"
                           @click.native="openQuestionPreview(question)">
                    <question-preview class="questionCard"
                                      :data="question"></question-preview>
                </md-layout>
            </md-layout>
        </md-layout>
    </div>
</template>

<style scoped>
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
    
    
    .question {
        width: 100%;
        flex-basis: 100%;
    }
    
    .questionContainer {
        min-width: 100%;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle } from "av-ts";
    import ActionButtons from "../util/ActionButtons.vue";
    import QuestionSearch from "./QuestionSearch.vue";
    import QuestionPreview from "./QuestionPreview.vue";
    import Question from "./Question.vue";

    import { Question as QuestionModel } from "../../interfaces/models";
    import QuestionRepository from "../../repositories/QuestionRepository";

    @Component({
        components: {
            ActionButtons,
            QuestionSearch,
            QuestionPreview,
            Question
        }
    })
    export default class QuestionBrowser extends Vue {
        questions: QuestionModel[] = [];

        showQuestions: QuestionModel[] = [];

        selectedQuestion: QuestionModel = null;
        userIsFinished: boolean = false;

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
