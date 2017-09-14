<template>
    <md-layout md-flex="100">
        <ul class="questionResponse">
            <li v-for="(possibleAnswer, index) in question.distractors"
                :key="index"
                :class="getResponseStyles(possibleAnswer)">
                <div v-if="disabledResponses.find(x => x == possibleAnswer) || userHasCorrectAnswer"
                     class="answerOption">
                    <div class="answerIcon">
                        <md-icon>{{ optionIcon(possibleAnswer) }}</md-icon>
                    </div>
                    <span>{{String.fromCharCode('A'.charCodeAt(0) + index)}}. {{possibleAnswer.content}}</span>
                </div>
                <md-checkbox v-else-if="Array.isArray(question.solution)"
                             :disabled="!!disabledResponses.find(x => x == possibleAnswer)"
                             :name="index"
                             :id="possibleAnswer.id">{{index}}</md-checkbox>
                <md-radio v-else
                          class="answerOption"
                          :disabled="!!disabledResponses.find(x => x == possibleAnswer)"
                          :md-value="index"
                          v-model="questionResponse"
                          name="answer"
                          @click.native="clickedResponse"
                          :id="'' + possibleAnswer.id">{{String.fromCharCode('A'.charCodeAt(0) + index)}}. {{possibleAnswer.content}}
                </md-radio>
                <div class="distributionOverlay"
                     :style="answerOptionFill(possibleAnswer)"></div>
            </li>
        </ul>
        <transition name="feedbackGroup"
                    @enter="feedbackEnter"
                    @leave="feedbackLeave"
                    :css="false">
            <md-layout md-flex="100"
                       md-gutter="8"
                       v-if="userHasCorrectAnswer">
                <md-layout md-flex="100"
                           class="componentSeparator"
                           md-gutter>
                    <md-card>
                        <h2>{{userHasCorrectAnswer ? "Correct" : "Incorrect"}}</h2>
                        <p v-if="userHasCorrectAnswer">{{ question.explanation }}</p>
                    </md-card>
                </md-layout>

                <md-layout md-flex="100"
                           md-gutter
                           class="componentSeparator">
                    <md-card class="placeBetween">
                        <question-rater icon="school"
                                        :rateAction="rate('difficulty')"
                                        :defaultValue="question.difficulty">Rate Difficulty</question-rater>
                        <question-rater class="ratingCard"
                                        :rateAction="rate('quality')"
                                        :defaultValue="question.quality">Rate Quality</question-rater>
                    </md-card>
                </md-layout>
            </md-layout>
        </transition>
    </md-layout>
</template>

<style scoped>
.questionResponse {
    list-style: none;
    margin: 0px;
    padding: 0px;
    width: 100%;
    margin-bottom: 1em;
    margin-top: 1em;
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
    padding: 1em 2em;
    display: flex;
    align-items: center;
    border: 1px solid #ddd;
    margin: 0px 8px 16px 0;
}

.answerOption .answerIcon {
    margin-left: -4px;
    margin-right: 15px;
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

.incorrect .distributionOverlay {
    background-color: rgba(255, 0, 0, 0.2);
}

.correct .distributionOverlay {
    background-color: rgba(34, 85, 102, 0.4);
}

h2 {
    margin: 0px;
    width: 100%;
}

.correctFill {
    background-color: rgba(34, 85, 102, 0.4) !important;
    min-width: 100%;
}

.placeBetween {
    justify-content: space-between;
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
import QuestionRater from "./QuestionRater.vue";
import QuestionService from "../../services/QuestionService";
import * as d3 from "d3";

@Component({
    components: {
        "question-rater": QuestionRater,
        "comment": Comment
    }
})
export default class QuestionResponse extends Vue {
    @Prop question: Question;

    userAnswer: number = -1;
    hasGivenUp = false;
    disabledResponses = [];

    feedbackEnter(el: HTMLElement, done) {
        el.style.height = "auto";
        const actualHeight = el.clientHeight;
        el.style.height = "0px";
        d3.select(el)
            .style("overflow", "hidden")
            .style("padding-top", "0")
            .style("padding-bottom", "0")
            .transition()
            .style("height", actualHeight + "px")
            .style("opacity", 1)
            .style("margin-bottom", "1em")
            .style("padding-top", "16px")
            .style("padding-bottom", "16px")
            .duration(500)
            .on("end", () => {
                el.style.height = "auto";
                done();
            });
    }

    feedbackLeave(el: HTMLElement, done) {
        d3.select(el)
            .transition()
            .style("height", "0px")
            .style("opacity", 0)
            .duration(500)
            .on("end", () => {
                done();
            });
    }

    getResponseStyles(answer) {
        const answerIcon = this.optionIcon(answer);
        return {
            answered: this.disabledResponses.find(x => x == answer) || this.userHasCorrectAnswer,
            correct: answerIcon == "done",
            incorrect: answerIcon != "done"
        };
    }

    // Getter/Setter for radio buttons
    get questionResponse() {
        return this.userAnswer;
    }

    set questionResponse(newValue) {
        const distractor = this.question.distractors[newValue];
        this.disabledResponses.push(distractor);
        this.userAnswer = newValue;

        QuestionService.submitResponse({ responseId: distractor.id })
            .then(x => {
                this.$emit("userAnswer", this.userHasCorrectAnswer);
            });
    }

    answerOptionFill(response) {
        if (this.userHasCorrectAnswer) {
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
        return this.question.solution == solution ? "done" : "clear";
    }

    get userHasCorrectAnswer() {
        return this.question.distractors[this.questionResponse] == this.question.solution;
    }

    resetAnswer() {
        this.disabledResponses.push(this.question.distractors[this.questionResponse]);
        this.questionResponse = -1;
    }

    // Bubble event down to radio button
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

    rate(rateType: string) {
        return rateValue => {
            QuestionService.submitRating({
                responseId: this.question.distractors[this.userAnswer].id,
                rateType: rateType,
                rateValue: rateValue
            });
        };
    }

}
</script>
