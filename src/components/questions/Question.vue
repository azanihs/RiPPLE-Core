<template>
    <md-layout class="container">
        <md-layout md-flex="65">
            <p class="questionContent">{{question.content}}</p>
        </md-layout>
        <md-layout class="questionInfo"
                   md-column>
            <md-card class="card">
                <md-card-header class="cardHeader">
                    <md-card-header-text>
                        <div class="md-title">Question Difficulty</div>
                    </md-card-header-text>
    
                    <md-card-media class="cardIcon">
                        <md-icon>school</md-icon>
                    </md-card-media>
                </md-card-header>
    
                <md-card-actions class="cardAction">
                    <rating :max="10"
                            :disabled="!userIsFinishedWithQuestion"
                            icon="school"
                            :defaultIndex="question.difficulty"></rating>
                </md-card-actions>
            </md-card>
            <md-card class="card">
                <md-card-header class="cardHeader">
                    <md-card-header-text>
                        <div class="md-title">Question Quality</div>
                    </md-card-header-text>
    
                    <md-card-media class="cardIcon">
                        <md-icon>star</md-icon>
                    </md-card-media>
                </md-card-header>
                <md-card-actions class="cardAction">
                    <rating :max="10"
                            :disabled="!userIsFinishedWithQuestion"
                            :defaultIndex="question.quality"></rating>
                </md-card-actions>
            </md-card>
        </md-layout>
        <question-response :question="question"
                           @userAnswer="updateUserAnswer"></question-response>
    </md-layout>
</template>

<style scoped>
    h2,
    h3 {
        width: 100%;
    }
    
    h3 {
        margin-top: 0px;
    }
    
    .container {}
    
    .questionContent {
        margin-top: 0px;
    }
    
    .md-chip.topicChip {
        margin-left: 10px;
        cursor: pointer;
        background-color: #fefefe;
        border: 1px solid #ccc;
        transition: 500ms ease background-color;
    }
    
    .md-primary {
        background-color: #256;
        color: #fff;
    }
    
    .questionInfo {
        align-items: stretch;
        margin-left: 2.5%;
        min-width: 32.5%;
        flex: 0 1 32.5%;
    }
    
    .card {
        position: relative;
        left: 0px;
        transition: left 500ms ease;
    }
    
    .card:not(:first-of-type) {
        margin-top: 2em;
    }
    
    .cardIcon {
        text-align: right;
        height: auto !important;
    }
    
    .cardHeader {
        align-items: center;
    }
    
    .md-title {
        margin-top: 0px !important;
    }
    
    .cardAction {
        justify-content: flex-start !important;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
    import { Question as QuestionModel } from "../../interfaces/models";

    import Rating from "./Rating.vue";
    import QuestionResponse from "./QuestionResponse.vue";

    import QuestionService from "../../services/QuestionService";

    @Component({
        components: {
            "rating": Rating,
            "question-response": QuestionResponse
        }
    })
    export default class Question extends Vue {
        @Prop question = p({
            required: true
        }) as QuestionModel;

        // question = QuestionService.getQuestion(this.type);
        userQualityRating: string = null;
        userIsFinishedWithQuestion: boolean = false;

        changeQualityRating(newRating: string) {
            this.userQualityRating = newRating;
        }

        updateUserAnswer(n: boolean) {
            this.userIsFinishedWithQuestion = n;
        }

    }
</script>
