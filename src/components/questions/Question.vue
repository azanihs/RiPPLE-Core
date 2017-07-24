<template>
    <md-layout class="container">
                    <div class="placeBetween">
                        <span>
                            <span>{{ question.responses.length }}
                                <md-icon>reply</md-icon>
                            </span>
                            <md-tooltip md-direction="top">Question Responses</md-tooltip>
                        </span>
                        <span class="difficulty">
                            <md-tooltip md-direction="top">Question Difficulty</md-tooltip>
                            <span>{{ question.difficultyRepresentation }}
                                <md-icon>school</md-icon>
                            </span>
                        </span>
                    </div>
                    <hr></hr>
                    <div class="placeBetween">
                        <span class="quality">
                            <md-tooltip md-direction="bottom">Question Quality</md-tooltip>
                            <md-icon :key="star"
                                     v-for="star in getStarIcons(question.quality)">{{ star }}</md-icon>
                        </span>
                        <span>
                            <router-link v-for="topic in question.topics"
                                         :key="topic"
                                         to="/view/questions"
                                         class="topicChipLink">
                                <md-chip class="topicChip">{{ topic }}</md-chip>
                            </router-link>
                        </span>
                    </div>
        <md-layout md-flex="100">
            <p class="questionContent">{{question.content}}</p>
        </md-layout>
        <question-response :question="question"
                           @userAnswer="updateUserAnswer">
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
        </question-response>
                           

    </md-layout>
</template>

<style scoped>

.placeBetween {
        justify-content: space-between !important;
        display: flex;
        padding-bottom: 0px;
        align-items: center;
        width: 100%;
}

.placeAround {
        justify-content: space-around !important;
        display: flex;
        padding-bottom: 0px;
        align-items: center;
        width: 100%;
}

    hr {
        border: none;
        border-bottom: 1px solid #ccc;
        width: 100%;
    }
    h2,
    h3 {
        width: 100%;
    }
    
    h3 {
        margin-top: 0px;
    }
    
    .container {}
    
    .questionContent {
        margin-top: 2em;
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
        width: 100%;
        background-color: transparent !important;;
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
            
            this.$emit("userAnswer", n);
        }
        
        
        getStarIcons(value: number): string[] {
            let stars = [];
            let numberStars;

            if (value % 2 == 0) {
                numberStars = value / 2;
                stars = new Array(numberStars).fill("star");
                stars = stars.concat(
                    new Array(5 - numberStars).fill("star_border")
                );
            } else {
                numberStars = (value - 1) / 2;
                stars = new Array(numberStars).fill("star");
                stars.push("star_half");
                stars = stars.concat(
                    new Array(4 - numberStars).fill("star_border")
                );
            }

            return stars;
        }

    }
</script>
