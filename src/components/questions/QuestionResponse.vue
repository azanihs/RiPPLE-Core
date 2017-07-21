<template>
    <md-tabs md-fixed
             class="md-transparent responseSection">
        <md-tab md-label="Respond To Question">
            <h3>Question Responses: </h3>
            <md-card v-if="userHasAnsweredQuestion"
                     class="md-primary questionExplanation">
                <md-card-header>
                    <div class="md-title">Title goes here</div>
                    <div class="md-subhead">Subtitle here</div>
                </md-card-header>
    
                <md-card-content>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit. Optio itaque ea, nostrum odio. Dolores, sed accusantium quasi non, voluptas eius illo quas, saepe voluptate pariatur in deleniti minus sint. Excepturi.
                </md-card-content>
                <md-card-actions class="cardAction"
                                 v-if="!userHasCorrectAnswer">
                    <md-button @click="resetAnswer">Try Again</md-button>
                    <md-button @click="hasGivenUp = true">Show Answer</md-button>
                </md-card-actions>
            </md-card>
            <ul class="questionResponse">
                <li v-for="(answer, index) in question.possibleAnswers"
                    :key="answer">
                    <div v-if="bluredItems.find(x => x == answer) || userIsFinishedAnswering"
                         class="answerOption">
                        <div class="answerIcon">
                            <md-icon>{{ optionIcon(answer) }}</md-icon>
                        </div>
                        <span>{{String.fromCharCode('A'.charCodeAt(0) + index)}}. {{answer.content}}</span>
                    </div>
                    <md-checkbox v-else-if="Array.isArray(question.solution)"
                                 :disabled="!!bluredItems.find(x => x == answer)"
                                 :name="index"
                                 :id="answer.id">{{index}}</md-checkbox>
                    <md-radio v-else
                              class="answerOption"
                              :disabled="!!bluredItems.find(x => x == answer)"
                              :md-value="index"
                              v-model="questionResponse"
                              name="answer"
                              @click.native="clickedResponse"
                              :id="'' + answer.id">{{String.fromCharCode('A'.charCodeAt(0) + index)}}. {{answer.content}}
                    </md-radio>
                    <div class="distributionOverlay"
                         :style="answerOptionFill(answer)"></div>
                </li>
            </ul>
            <div class="questionReview">
                <h4>{{userHasCorrectAnswer ? "Correct" : "Incorrect"}}</h4>
                <p>{{ question.explanation }}</p>
            </div>
        </md-tab>
        <md-tab md-label="Discussion">
            <h3>Question Discussion</h3>
            <div class="questionComments">
                <comment v-for="response in question.responses.slice(0, 10)"
                         class="commentCard"
                         :key="response"
                         :comment="response"></comment>
            </div>
        </md-tab>
    </md-tabs>
</template>

<style scoped>
    .md-tabs {
        border-top: 1px solid rgba(0, 0, 0, .12);
    }
    
    .cardAction {
        max-height: 100px;
    }
    
    .md-card.md-primary {
        background-color: #256 !important;
    }
    
    .questionResponse {
        list-style: none;
        margin: 0px;
        padding: 0px;
    }
    
    .questionResponse li {
        list-style: none;
        cursor: pointer;
        position: relative;
    }
    
    .answerOption {
        width: 100%;
        cursor: pointer;
        padding: 2em;
        display: flex;
        align-items: center;
        background-color: #fefefe;
        border: 1px solid #ddd;
    }
    
    .distributionOverlay {
        height: 100%;
        width: 0px;
        position: absolute;
        top: 0px;
        left: 0px;
        background-color: rgba(34, 85, 102, 0.4);
        transition: width 750ms ease;
        pointer-events: none;
    }
    
    .responseSection {
        width: 100%;
        margin-top: 2em;
    }
    
    .questionReview h4 {
        width: 100%;
        padding: 1em;
    }
    
    .questionComments {
        width: 100%;
    }
    
    .commentCard {
        width: 100%;
        margin-bottom: 16px;
    }
    
    .answerIcon {
        margin-right: 4px;
    }
</style>
<style>
    .responseOption .md-radio-label {
        height: auto !important;
        padding-left: 0px;
        margin-left: 0.5em;
    }
    
    .responseOption .md-radio-container {
        min-width: 20px;
        min-height: 20px;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle, Watch, Prop, p } from "av-ts";
    import { Question } from "../../interfaces/models";
    import Comment from "../util/Comment.vue";
    import QuestionService from "../../services/QuestionService";

    @Component({
        components: {
            "comment": Comment
        }
    })
    export default class QuestionResponse extends Vue {
        @Prop question: Question;

        userAnswer: number = -1;
        hasGivenUp = false;
        bluredItems = [];


        set questionResponse(newValue) {
            this.bluredItems.push(this.question.possibleAnswers[newValue]);
            this.userAnswer = newValue;
        }

        get questionResponse() {
            return this.userAnswer;
        }

        answerOptionFill(response) {
            if (this.userIsFinishedAnswering) {
                return {
                    width: (QuestionService.distributionForQuestion(this.question).get(response) * 100) + "%"
                };
            }

            return {};
        }

        optionIcon(solution) {
            if (Array.isArray(this.question.solution)) {
                return this.question.solution.find(x => x == solution.id) ? "done" : "clear";
            }
            return this.question.solution == solution.id ? "done" : "clear";
        }

        get userHasAnsweredQuestion() {
            return this.hasGivenUp || this.questionResponse != -1;
        }

        get userIsFinishedAnswering() {
            return this.hasGivenUp || this.userHasCorrectAnswer;
        }

        get userHasCorrectAnswer() {
            return this.question.solution == this.questionResponse;
        }

        get userFrustration() {
            return this.hasGivenUp;
        }

        resetAnswer() {
            this.bluredItems.push(this.question.possibleAnswers[this.questionResponse]);
            this.questionResponse = -1;
        }

        clickedResponse(e: MouseEvent) {
            const target = e.target as HTMLElement;
            if (target.tagName != "LABEL" && target.tagName != "INPUT") {
                const input = target.querySelector("input");
                const event = new MouseEvent("click", {
                    bubbles: true
                });
                input.dispatchEvent(event);
            }
        }
    }
</script>
