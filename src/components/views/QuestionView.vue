<template>
    <md-layout>
        <md-layout class="headingContainer">
            <h1>Questions</h1>
            <question-search :availableQuestions="questions" @searched="changeDisplay"/>
        </md-layout>
        <md-layout md-gutter="16" md-flex="100">
            <md-layout md-flex="33" v-for="question in showQuestions" :key="question.id">
                <md-card class="questionCard">
                    <md-card-area md-inset class="fullHeight">
                        <md-card-content class="fullHeight">
                            <div v-if="question.images.length > 0" class="cardPreview fullHeight">
                                <div ref="clamp" class="clamp">
                                    <img  :src="question.images[0]" />{{ question.content }}
                                </div>
                            </div>
                            <div v-else class="cardPreview fullHeight">
                                <div ref="clamp" class="clamp">{{ question.content }}</div>
                            </div>
                        </md-card-content>
                    </md-card-area>
                    <div class="pintoBottom">
                        <md-card-area>
                            <md-card-content>
                                <div class="placeAround">
                                    <span>
                                        <span>{{ question.responseCount }} <md-icon>reply</md-icon></span>
                                        <md-tooltip md-direction="top">Question Responses</md-tooltip>
                                    </span>
                                    <span>
                                        <md-tooltip md-direction="top">Question Difficulty</md-tooltip>
                                        <span>{{ getDifficultyText(question.difficulty) }} <md-icon>school</md-icon></span>
                                    </span>
                                </div>
                                <hr />
                                <div class="placeAround">
                                    <span>
                                        <md-tooltip md-direction="bottom">Question Quality</md-tooltip>
                                        <md-icon v-for="star in getStarIcons(question.quality)">{{ star }}</md-icon>
                                    </span>
                                    <span>
                                        <router-link v-for="topic in question.topics" :key="topic" to="/view/questions" class="topicChipLink">
                                            <md-chip class="topicChip">{{ topic }}</md-chip>
                                        </router-link>
                                    </span>
                                </div>
                            </md-card-content>
                        </md-card-area>
                    </div>
                </md-card>
            </md-layout>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .headingContainer {
        border-bottom: 1px solid #222;
        margin: 8px;
    }
    .questionCard {
        min-width: 100%;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .fullHeight {
        height: 100%;
    }
    .cardPreview img {
        width: 50%;
        height: auto;
        float: left;
        border: 1px solid #bbb;
        padding-right: 10px;
        padding-bottom: 10px;
        margin-right: 10px;
    }
    .clamp {
        line-height: 20px;
        overflow-wrap: break-word;
        word-wrap: break-word;
    }

    .pintoBottom {
        margin-top: auto;
        padding-bottom: 8px;
    }
    .placeAround {
        justify-content: space-between !important;
        display: flex;
        padding-bottom: 0px;
        align-items: center;
    }
    .placeAround > span {
        cursor: pointer;
    }

    .questionCard a.topicChipLink,
    .questionCard a.topicChipLink:visited {
        color: #333;
        text-decoration: none;
        transition: 500ms ease background-color, 500ms ease color;
    }
    .questionCard a.topicChipLink:hover {
        color: #bbb;
        text-decoration: none;
    }
    .questionCard .topicChip {
        margin-left: 5px;
        background-color: #fff;
        border: 1px solid #ccc;
        transition: 500ms ease background-color;
    }
    .topicChip:hover {
        background-color: #333;
    }


    /* Remove bottom border added by vue-material */
    .md-card .md-card-area:after {
        background: none !important;
    }
    hr {
        border: none;
        border-bottom: 1px solid #ccc;
    }
    .truncate {
        white-space: pre;
        overflow: hidden;
        text-overflow: ellipsis;
        display: block;
    }
    .md-card .md-card-content:last-child {
        padding-bottom: 0px;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle } from "av-ts";
    import QuestionSearch from "./QuestionSearch";
    import { Question } from "../../interfaces/models";
    import QuestionRepository from "../../repositories/QuestionRepository";

    import lineClamp from "line-clamp";

    @Component({
        components: {
            QuestionSearch
        }
    })
    export default class QuestionView extends Vue {
        questions: Question[] = [];

        showQuestions: Question[] = [];

        @Lifecycle
        created() {
            this.questions = QuestionRepository.getMany(25);
        }

        changeDisplay(searchedQuestions: Question[]) {
            this.showQuestions = searchedQuestions;
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
                numberStars = (value-1) / 2;
                stars = new Array(numberStars).fill("star");
                stars.push("star_half");
                stars = stars.concat(
                    new Array(4 - numberStars).fill("star_border")
                );
            }

            return stars;
        }

        @Lifecycle
        updated() {
            (this.$refs["clamp"] as HTMLElement[]).forEach(element => {
                lineClamp(element.childNodes[0].parentElement, { lineCount: 10 });
            });
        }
    }
</script>
