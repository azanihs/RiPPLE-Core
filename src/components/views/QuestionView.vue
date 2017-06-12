<template>
    <md-layout>
        <md-layout class="headingContainer">
            <h1>Questions</h1>
            <question-search :availableQuestions="questions" @searched="changeDisplay"/>
        </md-layout>
        <md-layout md-gutter="16" md-flex="100">
            <md-layout md-flex="33" v-for="question in showQuestions" :key="question.id">
                <md-card md-with-hover class="questionCard">
                    <md-card-area md-inset>
                        <md-card-content>
                            <div class="md-subhead truncate">
                                <span class="truncate">{{ question.content }}</span>
                            </div>
                        </md-card-content>
                    </md-card-area>
                    <md-card-area md-inset>
                        <md-card-content class='actions'>
                                <div class="placeAround">
                                    <span class="topics">
                                        <md-icon>school</md-icon>
                                        <span v-for="topic in question.topics" :key="topic">{{ topic }}</span>
                                    </span>
                                    <span>{{ question.responseCount }} <md-icon>comment</md-icon></span>
                                </div>
                            </md-card-content>
                    </md-card-area>
                    <md-card-actions class="actions">
                        <div>
                            <md-tooltip md-direction="top">Question Quality ({{ question.quality }})</md-tooltip>
                            <md-icon>star</md-icon>
                            <md-progress :md-progress="question.quality * 10"></md-progress>
                        </div>
                        <div>
                            <md-tooltip md-direction="bottom">Question Difficulty  ({{ question.difficulty }})</md-tooltip>
                            <md-icon>edit</md-icon>
                            <md-progress :md-progress="question.difficulty * 10"></md-progress>
                        </div>
                    </md-card-actions>

                    <md-ink-ripple></md-ink-ripple>
                </md-card>
            </md-layout>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .topics span {
        margin-right: 5px;
    }

    .truncate {
        white-space: pre;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .headingContainer {
        border-bottom: 1px solid #222;
        margin: 8px;
    }

    .cardContainer {
        margin: 8px;
        flex: 1;
    }
    .questionCard {
        min-width: 100%;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .placeAround {
        justify-content: space-between !important;
        display: flex;
    }

    .questionCard .actions {
        opacity: 0.75;
        color: #1d323a;
        flex-wrap: wrap;
    }
    .questionCard .actions div {
        display: flex;
        flex: 100%;
        align-items: center;
    }
    .md-card .md-subhead {
        opacity: 0.75;
        color: #1d323a;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle } from "av-ts";
    import QuestionSearch from "./QuestionSearch";
    import { Question } from "../../interfaces/models";
    import QuestionRepository from "../../repositories/QuestionRepository";

    @Component({
        components: {
            QuestionSearch
        }
    })
    export default class QuestionView extends Vue {
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
