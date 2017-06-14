<template>
<md-card>
    <md-card-area md-inset class="fullHeight">
        <md-card-content class="fullHeight">
            <div v-if="data.images.length > 0" class="cardPreview fullHeight">
                <div ref="clamp" class="clamp">
                    <img  :src="data.images[0]" />{{ data.content }}
                </div>
            </div>
            <div v-else class="cardPreview fullHeight">
                <div ref="clamp" class="clamp">{{ data.content }}</div>
            </div>
        </md-card-content>
    </md-card-area>
    <div class="pintoBottom">
        <md-card-area>
            <md-card-content>
                <div class="placeAround">
                    <span>
                        <span>{{ data.responseCount }} <md-icon>reply</md-icon></span>
                        <md-tooltip md-direction="right">Question Responses</md-tooltip>
                    </span>
                    <span>
                        <md-tooltip md-direction="top">Question Difficulty</md-tooltip>
                        <span>{{ getDifficultyText(data.difficulty) }} <md-icon>school</md-icon></span>
                    </span>
                </div>
                <hr />
                <div class="placeAround">
                    <span>
                        <md-tooltip md-direction="bottom">Question Quality</md-tooltip>
                        <md-icon :key="star" v-for="star in getStarIcons(data.quality)">{{ star }}</md-icon>
                    </span>
                    <span>
                        <router-link v-for="topic in data.topics" :key="topic" to="/view/questions" class="topicChipLink">
                            <md-chip class="topicChip">{{ topic }}</md-chip>
                        </router-link>
                    </span>
                </div>
            </md-card-content>
        </md-card-area>
    </div>
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
    import { Vue, Component, Lifecycle, Prop } from "av-ts";
    import { Question } from "../../interfaces/models";

    import lineClamp from "line-clamp";

    @Component()
    export default class QuestionCard extends Vue {
        @Prop
        data: Question;

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

        clampLines = () => {
            const element = this.$refs["clamp"] as HTMLElement;
            lineClamp(element.childNodes[0].parentElement, { lineCount: 5 });
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
