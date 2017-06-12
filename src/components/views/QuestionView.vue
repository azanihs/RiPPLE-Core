<template>
    <md-layout>
        <md-layout class="headingContainer">
            <h1>Questions</h1>
        </md-layout>
        <md-layout md-gutter="16" md-flex="100">
            <md-layout md-flex="33" v-for="question in questions" :key="question.id">
                <md-card md-with-hover class="questionCard">
                    <md-card-area md-inset>
                        <md-card-header>
                            <div class="md-subhead placeAround">
                                <span>
                                    <md-icon :style="{ color: getColourFromValue(question.quality) }">
                                        {{ getIconFromQuality(question.quality) }}
                                    </md-icon>
                                </span>
                                <span>
                                    <md-icon v-for="star in getStarsFromDifficulty(question.difficulty)">
                                        {{ star }}
                                    </md-icon>
                                </span>
                            </div>
                        </md-card-header>
                        <md-card-content class="truncate">{{ question.content }}</md-card-content>
                    </md-card-area>

                    <md-card-actions class="actions placeAround">
                        <span><md-icon>school</md-icon> {{ question.topic }}</span>
                        <span><md-icon>comment</md-icon> {{ question.responseCount }}</span>
                    </md-card-actions>

                    <md-ink-ripple></md-ink-ripple>
                </md-card>
            </md-layout>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .truncate {
        white-space: pre;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .headingContainer {
        border-bottom: 1px solid #222;
        margin: 8px;
    }

    .cardContainer {
        margin: 8px;
        flex: 1;
    }
    .questionCard {
        min-width: 100%;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .placeAround {
        justify-content: space-between !important;
        display: flex;
    }

    .questionCard .actions {
        opacity: 0.75;
        color: #1d323a;
    }
    .md-card .md-subhead {
        opacity: 0.75;
        color: #1d323a;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle } from "av-ts";
    import QuestionRepository from "../../repositories/QuestionRepository";

    @Component()
    export default class QuestionView extends Vue {
        questions = null;

        @Lifecycle
        created() {
            this.questions = QuestionRepository.getMany(10);
        }

        getColourFromValue(value: number): string {
            if (value < 2.5) {
                return "#d6320e";
            } else if (value >= 2.5 && value < 5) {
                return "#c00d8a";
            } else if (value >= 5 && value < 7.5) {
                return "#3978ba";
            } else {
                return "#1d323a";
            }
        }

        getIconFromQuality(quality: number): string {
            if (quality < 2.5) {
                return "sentiment_very_dissatisfied";
            } else if (quality >= 2.5 && quality < 5) {
                return "sentiment_dissatisfied";
            } else if (quality >= 5 && quality < 7.5) {
                return "sentiment_satisfied";
            } else {
                return "sentiment_very_satisfied";
            }
        }

        getStarsFromDifficulty(difficulty: number): string[] {
            if (difficulty % 2 == 0) {
                return new Array(difficulty/2).fill("star");
            } else {
                const stars = new Array((difficulty-1)/2).fill("star");
                return stars.concat(["star_half"]);
            }
        }

    }
</script>
