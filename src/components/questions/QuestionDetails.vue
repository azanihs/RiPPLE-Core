<template>
    <md-layout md-flex="100">
        <div class="placeBetween">
            <div>
                <span>{{ question.responses.length }}
                    <md-icon>reply</md-icon>
                </span>
                <md-tooltip md-direction="top">Question Responses</md-tooltip>
            </div>
            <div>
                <span>{{ question.difficulty }}
                    <md-icon>school</md-icon>
                </span>
                <md-tooltip md-direction="top">Question Difficulty</md-tooltip>
            </div>
        </div>
        <hr />
        <div class="placeBetween">
            <div>
                <span>{{ question.quality }}
                    <md-icon>star</md-icon>
                </span>
                <md-tooltip md-direction="bottom">Question Quality</md-tooltip>
            </div>
            <div>
                <topic-chip v-for="topic in question.topics"
                            :key="topic.id"
                            linkTo="/view/questions">
                    {{topic.name}}
                </topic-chip>
            </div>
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

.placeBetween>div {
    cursor: pointer;
    color: #1d323a;
}

hr {
    border: none;
    border-bottom: 1px solid #ccc;
    width: 100%;
}
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { Question } from "../../interfaces/models";
import TopicChip from "../util/TopicChip.vue";

@Component({
    components: {
        TopicChip
    }
})
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
