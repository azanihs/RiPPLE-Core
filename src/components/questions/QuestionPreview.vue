<template>
    <div class="card">
        <div class="leftPanel fullHeight">
            <div ref="clamp" class="clamp">
                <img v-if="data.images.length > 0" :src="data.images[0]"></img>
                <span>{{ data.content }}</span>
            </div>
            <div class="bottomPanel">
                <router-link v-for="topic in data.topics" :key="topic" to="/view/questions" class="topicChipLink">
                    <md-chip class="topicChip">{{ topic }}</md-chip>
                </router-link>
            </div>
        </div>
        <md-layout class="rightPanel">
            <div>
                <md-icon>reply</md-icon>
                <span>{{ data.responses.length }}</span>
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
            <div>
                <md-icon>person_pin</md-icon>
                <span>{{ Math.floor(Math.random() * 10) }}</span>
                <md-tooltip md-direction="top">Question Suitability</md-tooltip>
            </div>
        </md-layout>
    
    </div>
</template>

<style scoped>
.card {
    border: 1px solid #ddd;
    display: flex;
    flex: 1;
    border-radius: 2px;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2), 0 2px 2px rgba(0, 0, 0, 0.14), 0 3px 1px -2px rgba(0, 0, 0, 0.12);
    height: 262px;
    cursor: pointer;
}

.leftPanel {
    padding: 8px;
    border-right: 1px solid #ddd;
}

.leftPanel img {
    width: 50%;
    height: auto;
    float: left;
    border: 1px solid #bbb;
    margin-right: 10px;
    box-shadow: 2px 2px 5px #aaa;
}

.rightPanel {
    padding: 8px;
    background-color: #fafafa;
    color: #999;
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
import { Vue, Component, Lifecycle, Prop } from "av-ts";
import { Question } from "../../interfaces/models";

import QuestionDetails from "./QuestionDetails.vue";

import lineClamp from "line-clamp";

@Component({
    components: {
        "question-details": QuestionDetails
    }
})
export default class QuestionPreview extends Vue {
    @Prop data: Question;

    clampLines = () => {
        /*const element = this.$refs["clamp"] as HTMLElement;
        if (element) {
            lineClamp(element.childNodes[0].parentElement, { lineCount: 5 });
        }*/
    }

    @Lifecycle
    mounted() {
        this.clampLines();
    }

    @Lifecycle
    updated() {
        this.clampLines();
    }
}
</script>
