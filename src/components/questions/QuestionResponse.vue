<template>
    <md-tabs md-fixed
             class="md-transparent responseSection">
        <md-tab md-label="Respond To Question">
            <transition name="feedbackGroup"
                        @enter="feedbackEnter"
                        @leave="feedbackLeave"
                        :css="false">
                <md-card v-if="userHasAnsweredQuestion"
                         :key="userIsFinishedAnswering"
                         class="md-primary questionExplanation">
                    <md-card-header>
                        <div class="md-title">{{userHasCorrectAnswer ? "Correct" : "Incorrect"}}</div>
                    </md-card-header>
    
                    <md-card-content>
                        <p v-if="userIsFinishedAnswering">{{ question.explanation }}</p>
                        <p v-else>
                            How about a slice of quiche?
                        </p>
                    </md-card-content>
                    <md-card-actions class="cardAction"
                                     v-if="!userHasCorrectAnswer">
                        <md-button @click="resetAnswer">Try Again</md-button>
                        <md-button @click="userGiveUp">Show Answer</md-button>
                    </md-card-actions>
                </md-card>
            </transition>
            <ul class="questionResponse">
                <li v-for="(answer, index) in question.possibleAnswers"
                    :key="answer"
                    :class="{answered: bluredItems.find(x => x == answer) || userIsFinishedAnswering, incorrect: optionIcon(answer) != 'done', correct: optionIcon(answer) == 'done'}">
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
    .questionExplanation {
        height: 0px;
        opacity: 0;
        overflow: hidden;
    }
    
    .md-tabs {
        border-top: 1px solid rgba(0, 0, 0, .12);
    }
    
    .cardAction {
        max-height: 100px;
    }
    
    .md-card.md-primary {
        background-color: #256 !important;
        margin-bottom: 1em;
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
        transition: background-color 500ms ease;
    }
    
    .answerOption {
        width: 100%;
        cursor: pointer;
        padding: 2em;
        display: flex;
        align-items: center;
        border: 1px solid #ddd;
    }
    
    .incorrect .distributionOverlay {
        background-color: rgba(255, 0, 0, 0.2);
    }
    
    .correct .distributionOverlay {
        background-color: rgba(34, 85, 102, 0.4);
    }
    
    .distributionOverlay {
        height: 100%;
        width: 0px;
        position: absolute;
        top: 0px;
        left: 0px;
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
    .answerOption .md-radio-label {
        height: auto !important;
        padding-left: 0px;
        margin-left: 0.5em;
    }
    
    .answerOption .md-radio-container {
        min-width: 20px;
        min-height: 20px;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle, Watch, Prop, p } from "av-ts";
    import { Question } from "../../interfaces/models";
    import Comment from "../util/Comment.vue";
    import QuestionService from "../../services/QuestionService";
    import * as d3 from "d3";

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


        feedbackEnter(el: HTMLElement, done) {
            el.style.height = "auto";
            const actualHeight = el.clientHeight;
            el.style.height = "0px";
            d3.select(el)
                .transition()
                .style("height", actualHeight + "px")
                .style("opacity", 1)
                .duration(500);
            setTimeout(() => done(), 500);
        }

        feedbackLeave(el: HTMLElement, done) {
            d3.select(el)
                .transition()
                .style("height", "0px")
                .style("opacity", 0)
                .duration(500);
            setTimeout(() => done(), 500);
        }

        @Watch("userAnswer")
        handleResponseChange() {

        }

        set questionResponse(newValue) {
            this.bluredItems.push(this.question.possibleAnswers[newValue]);
            this.userAnswer = newValue;

            this.$emit("userAnswer", this.userIsFinishedAnswering);
        }
        userGiveUp() {
            this.hasGivenUp = true;
            this.$emit("userAnswer", this.userIsFinishedAnswering);
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
