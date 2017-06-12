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
                            <div v-if="question.images.length > 0" class="md-subhead cardPreview cardPreviewImg fullHeight">
                                <img  :src="question.images[0]" />
                                <div ref="clamp_img" class="clamp">{{ question.content }}/</div>
                            </div>
                            <div v-else class="md-subhead cardPreview fullHeight">
                                <div ref="clamp" class="clamp">{{ question.content }}/</div>
                            </div>
                        </md-card-content>
                    </md-card-area>
                    <div class="pintoBottom">
                        <md-card-area md-inset>
                            <md-card-content>
                                <div class="placeAround">
                                    <span class="topics">
                                        <div class="topicContainer">
                                            <md-icon>school </md-icon>
                                            <router-link v-for="topic in question.topics" :key="topic" to="/view/questions" class="topicChipLink">
                                                <md-chip class="topicChip">{{ topic }}</md-chip>
                                            </router-link>
                                        </div>
                                    </span>
                                    <span>
                                        <span>{{ question.responseCount }} <md-icon>comment</md-icon></span>
                                        <md-tooltip md-direction="bottom">Question Responses</md-tooltip>
                                    </span>
                                </div>
                            </md-card-content>
                        </md-card-area>
                        <md-card-actions class="actions charts">
                            <div>
                                <md-tooltip md-direction="top">Question Quality ({{ question.quality }})</md-tooltip>
                                <md-icon>star</md-icon>
                                <md-progress :md-progress="question.quality * 10"></md-progress>
                            </div>
                            <div>
                                <md-tooltip md-direction="bottom">Question Difficulty  ({{ question.difficulty }})</md-tooltip>
                                <md-icon>edit</md-icon>
                                <md-progress :md-progress="question.difficulty * 10"></md-progress>
                            </div>
                        </md-card-actions>
                    </div>

                </md-card>
            </md-layout>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .fullHeight {
        height: 100%;
    }
    .topics span {
        margin-right: 5px;
    }

    .truncate {
        white-space: pre;
        overflow: hidden;
        text-overflow: ellipsis;
        display: block;
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

    .pintoBottom {
        margin-top: auto;
        padding-bottom: 8px;
    }
    .questionCard .actions {
        color: #1d323a;
        flex-wrap: wrap;
    }

    .questionCard .actions.charts {
        padding: 16px;
    }

    .questionCard .actions div {
        display: flex;
        flex: 100%;
        align-items: center;
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

    .md-card .md-subhead {
        opacity: 1;
        color: #1d323a;
    }

    .cardPreview img {
        width: 200px;
        height: auto;
        float: left;
        margin-right: 10px;
        margin-bottom: 10px;
    }
    .clamp {
        line-height: 20px;
        overflow-wrap: break-word;
        word-wrap: break-word;
    }

    .md-card-content {
        padding-bottom: inherit !important;
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

        @Lifecycle
        updated() {
            (this.$refs["clamp"] as HTMLElement[]).forEach(element => {
                lineClamp(element.childNodes[0].parentElement, { lineCount: 5 });
            });
            (this.$refs["clamp_img"] as HTMLElement[]).forEach(element => {
                lineClamp(element.childNodes[0].parentElement, { lineCount: 3 });
            });
        }
    }
</script>
