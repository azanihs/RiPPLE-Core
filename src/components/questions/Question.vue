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
    </md-layout>
</template>

<style scoped>
    h2 {
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

        changeQualityRating(newRating: string) {
            this.userQualityRating = newRating;
        }

        get question() {
            return QuestionService.getQuestion(this.type);
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

        getDifficultyText(difficulty: number): string {
            if (difficulty <= 3.3) {
                return "Easy";
            } else if (difficulty > 3.3 && difficulty <= 6.6) {
                return "Medium";
            } else {
                return "Hard";
            }
        }
    }
</script>
