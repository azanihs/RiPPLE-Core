<template>
    <md-card md-with-hover
             class="card">
        <div class="cardContainer">
            <div class="leftPanel fullHeight">
                <div ref="clamp"
                     class="clamp">
                    <span v-html="data.content"></span>
                </div>
                <div class="bottomPanel">
                    <topic-chip v-for="topic in data.topics"
                                :disabled="true"
                                :key="topic.id">
                        {{topic.name}}
                    </topic-chip>
                </div>
            </div>
            <md-layout class="rightPanel">
                <div>
                    <md-icon>reply</md-icon>
                    <span>{{ data.responseCount }}</span>
                    <md-tooltip md-direction="top">Question Responses</md-tooltip>
                </div>
                <div>
                    <md-icon>school</md-icon>
                    <span>{{ data.difficulty }}</span>
                    <md-tooltip md-direction="top">Question Difficulty</md-tooltip>
                </div>
                <div>
                    <md-icon>star</md-icon>
                    <span>{{ data.quality }}</span>
                    <md-tooltip md-direction="top">Question Quality</md-tooltip>
                </div>
            </md-layout>
        </div>
    </md-card>
</template>

<style>
.leftPanel img {
    width: 50%;
    max-height: 95% !important;
    float: left;
    border: 1px solid #bbb;
    margin-right: 10px;
    box-shadow: 2px 2px 5px #aaa;
}
</style>

<style scoped>
.card {
    padding: 0px !important;
    overflow-y: hidden;
}

.cardContainer {
    display: flex;
    flex: 1;
    height: 262px;
    cursor: pointer;
}

.leftPanel {
    padding: 8px;
    border-right: 1px solid #ddd;
    flex: 1;
}

.rightPanel {
    padding: 8px;
    background-color: #fafafa;
    color: #999;
    flex-grow: 0;
}

.rightPanel>div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.rightPanel i {
    margin: 0px;
}

.clamp {
    overflow: hidden;
    text-overflow: ellipsis;
    height: 200px;
}

.bottomPanel {
    margin-top: 10px;
    width: 100%;
}

.topics {
    margin-bottom: 5px;
}
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { IQuestion } from "../../interfaces/models";

import QuestionDetails from "./QuestionDetails.vue";
import TopicChip from "../util/TopicChip.vue";

@Component({
    components: {
        QuestionDetails,
        TopicChip
    }
})
export default class QuestionPreview extends Vue {
    @Prop data = p<IQuestion>({
        required: true
    });
}
</script>
