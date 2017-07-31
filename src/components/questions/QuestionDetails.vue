<template>
    <md-layout md-flex="100">
        <div class="placeBetween">
            <span>
                <span>{{ question.responses.length }}
                    <md-icon>reply</md-icon>
                </span>
                <md-tooltip md-direction="top">Question Responses</md-tooltip>
            </span>
            <span>
                <md-tooltip md-direction="top">Question Difficulty</md-tooltip>
                <span>{{ question.difficultyRepresentation }}
                    <md-icon>school</md-icon>
                </span>
            </span>
        </div>
        <hr></hr>
        <div class="placeBetween">
            <span>
                <md-tooltip md-direction="bottom">Question Quality</md-tooltip>
                <md-icon :key="star" v-for="star in starIcons">{{ star }}</md-icon>
            </span>
            <span>
                <router-link v-for="topic in question.topics" :key="topic" to="/view/questions" class="topicChipLink">
                    <md-chip class="topicChip">{{ topic }}</md-chip>
                </router-link>
            </span>
        </div>
    </md-layout>
</template>

<style scoped>
.placeBetween {
    justify-content: space-between;
    display: flex;
    padding-bottom: 0px;
    align-items: center;
    width: 100%;
}

.placeBetween>span {
    cursor: pointer;
}

hr {
    border: none;
    border-bottom: 1px solid #ccc;
    width: 100%;
}

.md-chip.topicChip {
    margin-right: 5px;
    cursor: pointer;
    background-color: #ffffff;
    border: 1px solid #ccc;
    transition: 500ms ease background-color;
}

a.topicChipLink,
a.topicChipLink:visited {
    color: #333;
    text-decoration: none;
    transition: 500ms ease background-color, 500ms ease color;
}

a.topicChipLink:hover {
    color: #bbb;
    text-decoration: none;
}

.topicChip:hover {
    background-color: #333;
}
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { Question } from "../../interfaces/models";

@Component()
export default class QuestionDetails extends Vue {
    @Prop question = p({
        required: true
    }) as Question;


    get starIcons(): string[] {
        const value = this.question.quality;
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
