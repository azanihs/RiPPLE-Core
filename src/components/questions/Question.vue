<template>
    <md-layout>
        <md-layout md-flex="100">
            <p class="questionContent">
                <img v-if="question.images.length > 0" :src="question.images[0]"></img>
                {{question.content}}
            </p>
        </md-layout>
        <question-details :question="question"></question-details>
        <question-response :question="question" @userAnswer="updateUserAnswer">
        </question-response>
    
    </md-layout>
</template>

<style scoped>
img {
    width: 25%;
    height: auto;
    float: left;
    border: 1px solid #bbb;
    padding-right: 10px;
    padding-bottom: 10px;
    margin-right: 10px;
}

.questionContent {
    margin-top: 2em;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import { Question as QuestionModel } from "../../interfaces/models";

import QuestionDetails from "./QuestionDetails.vue";
import QuestionResponse from "./QuestionResponse.vue";
import QuestionService from "../../services/QuestionService";

@Component({
    components: {
        "question-response": QuestionResponse,
        "question-details": QuestionDetails
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
