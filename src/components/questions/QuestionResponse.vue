<template>
    <md-tabs md-fixed
             class="md-transparent responseSection">
        <md-tab md-label="Respond To Question">
            <h3>Question Responses: </h3>
            <ul class="questionResponse">
                <li v-for="(response, index) in question.possibleAnswers"
                    :key="response.id">
                    <md-checkbox v-if="Array.isArray(question.solution)"
                                 :name="index"
                                 :id="response.id">{{index}}</md-checkbox>
                    <md-radio v-else
                              class="responseOption"
                              :md-value="index"
                              v-model="questionResponse"
                              name="response"
                              @click.native="clickedResponse"
                              :id="'' + response.id">{{String.fromCharCode('A'.charCodeAt(0) + index)}}. {{response.content}}
                    </md-radio>
                </li>
            </ul>
            <div class="questionReview">
                <h4>{{userHasCorrectAnswer ? "Correct" : "Incorrect"}}</h4>
                <p>{{ question.explanation }}</p>
            </div>
            <div>
                Breakdown/Pie chart Answer distribution
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
    
    .questionResponse {
        list-style: none;
        margin: 0px;
        padding: 0px;
    }
    
    .questionResponse li {
        list-style: none;
        cursor: pointer;
    }
    
    .responseOption {
        width: 100%;
        cursor: pointer;
        padding: 2em;
        display: flex;
        align-items: center;
        background-color: #fefefe;
        border: 1px solid #ddd;
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
    import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
    import { Question } from "../../interfaces/models";
    import Comment from "../util/Comment.vue";

    @Component({
        components: {
            "comment": Comment
        }
    })
    export default class QuestionResponse extends Vue {
        @Prop question: Question;

        questionResponse: number = -1;
        get userHasAnsweredQuestion() {
            return this.questionResponse != -1;
        }

        get userHasCorrectAnswer() {
            return this.question.solution == this.questionResponse;
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
