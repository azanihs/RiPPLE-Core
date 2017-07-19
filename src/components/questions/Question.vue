<template>
    <md-layout>
        <h2>Recommended Question for topic
            <md-chip v-for="topic in question.topics"
                     :key="topic"
                     class="topicChip">{{topic}}</md-chip>
        </h2>
        <md-layout md-flex="65">
            <p>{{question.content}}</p>
    
        </md-layout>
        <md-layout md-flex="10"></md-layout>
        <md-layout class="questionInfo"
                   md-flex="25"
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
                            :defaultIndex="question.quality"></rating>
                </md-card-actions>
            </md-card>
        </md-layout>
    
        <md-layout>
            <h3>Question Responses</h3>
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
        </md-layout>
    </md-layout>
</template>

<style scoped>
    h2,
    h3 {
        width: 100%;
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
        background-color: #fefefe;
        border: 1px solid #ddd;
    }
</style>


<script lang="ts">
    import { Vue, Component, Prop, p } from "av-ts";
    import Rating from "./Rating.vue";
    import QuestionService from "../../services/QuestionService";

    @Component({
        components: {
            "rating": Rating
        }
    })
    export default class Question extends Vue {
        @Prop type = p({
            type: String,
            default: "random"
        }) as string;

        userQualityRating: string = null;
        questionResponse: number = -1;

        changeQualityRating(newRating: string) {
            this.userQualityRating = newRating;
        }

        get question() {
            return QuestionService.getQuestion(this.type);
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
