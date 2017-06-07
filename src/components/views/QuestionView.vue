<template>
    <md-layout>
        <md-layout class="headingContainer">
            <h1>Questions</h1>
        </md-layout>
        <md-layout md-gutter="16" md-flex="100">
            <md-layout md-flex="33" v-for="question in questions" :key="question.id">
                <md-card md-with-hover class="questionCard">
                    <md-card-area md-inset>
                        <md-card-media md-ratio="16:9">
                            <img src="https://placebear.com/g/200/300" alt="Question image">
                        </md-card-media>

                        <md-card-header>
                            <h2 class="truncate md-title">{{ question.title }} </h2>
                            <div class="md-subhead">
                                <md-icon>star rate</md-icon>
                                <span>{{ question.difficulty }}</span>
                            </div>
                        </md-card-header>

                        <md-card-content class="truncate">{{ question.content }}</md-card-content>
                    </md-card-area>

                    <md-card-actions class="actions">
                        <span><md-icon>school</md-icon> {{ question.topic }}</span>
                        <span><md-button class="md-primary">View</md-button></span>
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
    .questionCard .actions {
        justify-content: space-between;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle } from "av-ts";
    import QuestionRepository from "@/repositories/QuestionRepository";

    @Component()
    export default class QuestionView extends Vue {
        questions = null;

        @Lifecycle
        created() {
            this.questions = QuestionRepository.getMany(10);
        }
    }
</script>
