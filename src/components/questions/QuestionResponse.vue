<template>
    <md-layout md-flex="100">
        <ul class="questionResponse">
            <li v-for="(possibleAnswer, index) in question.possibleAnswers" :key="index" :class="getResponseStyles(possibleAnswer)">
                <div v-if="disabledResponses.find(x => x == possibleAnswer) || userHasCorrectAnswer" class="answerOption">
                    <div class="answerIcon">
                        <md-icon>{{ optionIcon(possibleAnswer) }}</md-icon>
                    </div>
                    <span>{{String.fromCharCode('A'.charCodeAt(0) + index)}}. {{possibleAnswer.content}}</span>
                </div>
                <md-checkbox v-else-if="Array.isArray(question.solution)" :disabled="!!disabledResponses.find(x => x == answer)" :name="index" :id="possibleAnswer.id">{{index}}</md-checkbox>
                <md-radio v-else class="answerOption" :disabled="!!disabledResponses.find(x => x == possibleAnswer)" :md-value="index" v-model="questionResponse" name="answer" @click.native="clickedResponse" :id="'' + possibleAnswer.id">{{String.fromCharCode('A'.charCodeAt(0) + index)}}. {{possibleAnswer.content}}
                </md-radio>
                <div class="distributionOverlay" :style="answerOptionFill(possibleAnswer)"></div>
            </li>
        </ul>
        <transition name="feedbackGroup" @enter="feedbackEnter" @leave="feedbackLeave" :css="false">
            <md-tabs v-if="userHasCorrectAnswer" md-fixed class="md-transparent responseSection">
                <md-tab md-label="Explanation">
                    <md-layout>
                        <div class="placeBetween">
                            <md-layout md-flex="65" class="questionExplanation">
                                <h2>{{userHasCorrectAnswer ? "Correct" : "Incorrect"}}</h2>
                                <p v-if="userHasCorrectAnswer">{{ question.explanation }}</p>
                            </md-layout>
                            <md-layout md-flex-offset="10" md-flex="25">
                                <question-rater icon="school" :defaultValue="question.difficulty">Rate Difficulty</question-rater>
                                <question-rater class="ratingCard" :defaultValue="question.quality">Rate Quality</question-rater>
                            </md-layout>
                        </div>
                    </md-layout>
                </md-tab>
                <md-tab md-label="Discussion">
                    <h3>Question Discussion</h3>
                    <div class="commentContainer">
                        <comment v-for="response in question.responses.slice(0, 10)" class="commentCard" :key="response.id" :comment="response"></comment>
                    </div>
                </md-tab>
            </md-tabs>
        </transition>
    </md-layout>
</template>

<style scoped>
.responseSection {
    margin-top: 2em;
}

.placeBetween {
    justify-content: space-between;
    display: flex;
    padding-bottom: 0px;
    align-items: flex-start;
    width: 100%;
}

.questionExplanation {
    border: 1px solid #ddd;
    padding: 1em;
    height: 100%;
}

.md-tabs {
    border-top: 1px solid rgba(0, 0, 0, .12);
}

.questionResponse {
    list-style: none;
    margin: 0px;
    padding: 0px;
    width: 100%;
    margin-top: 2em;
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

.answerOption .answerIcon {
    margin-right: 4px;
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

.commentContainer {
    width: 100%;
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
        const actualHeight = el.clientHeight + 20;
        el.style.height = "0px";
        d3.select(el)
            .transition()
            .style("height", actualHeight + "px")
            .style("opacity", 1)
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
        this.disabledResponses.push(this.question.possibleAnswers[newValue]);
        this.userAnswer = newValue;
        this.$emit("userAnswer", this.userHasCorrectAnswer);
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
        return this.question.solution == solution.id ? "done" : "clear";
    }

    get userHasCorrectAnswer() {
        return this.question.solution == this.questionResponse;
    }

    resetAnswer() {
        this.disabledResponses.push(this.question.possibleAnswers[this.questionResponse]);
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


}
</script>
