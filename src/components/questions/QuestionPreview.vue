<template>
    <md-card>
        <md-card-area md-inset class="fullHeight">
            <md-card-content class="fullHeight">
                <div class="cardPreview fullHeight">
                    <div ref="clamp" class="clamp">
                        <img v-if="data.images.length > 0" :src="data.images[0]"></img>
                        {{ data.content }}
                    </div>
                </div>
            </md-card-content>
        </md-card-area>
        <div class="pintoBottom">
            <md-card-area>
                <md-card-content>
                    <question-details :question="data"></question-details>
                </md-card-content>
            </md-card-area>
        </div>
        <md-ink-ripple></md-ink-ripple>
    </md-card>
</template>

<style scoped>
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

.md-card .md-card-area:after {
    /* Remove bottom border added by vue-material */
    background: none !important;
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
        const element = this.$refs["clamp"] as HTMLElement;
        if (element) {
            lineClamp(element.childNodes[0].parentElement, { lineCount: 5 });
        }
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
