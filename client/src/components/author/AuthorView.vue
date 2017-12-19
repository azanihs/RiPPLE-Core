<template>
    <md-layout :class="bottomSpaceClass">
        <md-layout md-hide-medium-and-up class="hidden" ref="onlyVisibleOnMobile"></md-layout>
        <md-layout md-flex="100">
            <md-tabs md-fixed
                :mdNavigation="false"
                class="md-transparent tabContainer"
                :class="{'mainTab': !mobileMode}"
                @change="tabSelected">
                    <md-tab md-label="Write Question">
                        <md-layout md-flex="100">
                            <md-card class="firstAuthorCard">
                                <md-layout md-flex="100"
                                    class="componentSeparator">
                                    <h2>Question Body</h2>
                                    <TinyMCE id="questionEditor"
                                        v-model="question.content"
                                        :options="options"></TinyMCE>
                                </md-layout>
                                <md-layout md-flex="100">
                                    <h2>Topics</h2>
                                    <topic-chip v-for="topic in topics"
                                        :key="topic.id"
                                        :disabled="!topicIsUsed(topic)"
                                        @click.native="toggleTopic(topic)">
                                        {{topic.name}}
                                    </topic-chip>
                                </md-layout>
                            </md-card>
                        </md-layout>
                        <md-layout md-flex="100"
                            class="cardSeparator">
                            <md-card class="removePadding">
                                <md-tabs md-fixed
                                    :mdNavigation="false"
                                    class="md-transparent tabContainer subTabs"
                                    :class = "{'subTabs': !mobileMode}">
                                    <md-tab v-for="i in ['A', 'B', 'C', 'D']"
                                        :key="i"
                                        :id="'tab_' + i"
                                        :md-label="'Response ' + i">
                                        <TinyMCE :id="'editor_' + i"
                                            v-model="question.responses[i]"
                                            :options="options"></TinyMCE>
                                    </md-tab>
                                </md-tabs>
                            </md-card>
                        </md-layout>
                        <md-layout md-flex="100"
                            class="cardSeparator">
                            <md-card>
                                <h3>Correct Answer</h3>
                                <md-layout md-flex="100"
                                    class="flexAround">
                                    <md-radio v-for="i in ['A', 'B', 'C', 'D']"
                                        :key="i"
                                        v-model="question.correctIndex"
                                        :md-value="i"
                                        name="correctQuestionGroup">{{i}}</md-radio>
                                </md-layout>
                            </md-card>
                        </md-layout>
                        <md-layout md-flex="100"
                            class="cardSeparator">
                            <md-card>
                                <md-layout md-flex="100"
                                    class="componentSeparator">
                                    <h2>Question Explanation</h2>
                                    <TinyMCE id="questionExplanation"
                                        v-model="question.explanation"
                                        :options="options"></TinyMCE>
                                </md-layout>
                            </md-card>
                        </md-layout>
                    </md-tab>
                    <md-tab
                        :md-label="prevLabel"
                        :md-disabled="prevDisabled">
                            <question v-if="questionPrev" :question="questionPrev"
                                :preview="true"
                                :showSpeedDial="false"
                                :showNavBar="false"></question>
                    </md-tab>
                </md-tabs>
            <md-layout md-flex="100"
                class="rightAlign">
                <div class="uploadContainer md-fab-bottom-right floatingAction">
                    <md-tooltip v-if="!uploadDone"
                        md-direction="top">Upload Question</md-tooltip>
                    <md-tooltip v-if="uploadDone"
                        md-direction="top">Question Uploaded</md-tooltip>
                    <md-button class="md-fab md-raised uploadButton"
                        @click="validateUpload"
                        :class="{'done': uploadDone}">
                        <md-icon v-if="!uploadDone">cloud_upload</md-icon>
                        <md-icon v-if="uploadDone">done</md-icon>
                    </md-button>
                    <md-spinner class="progressSpinner uploadSpinner"
                        :md-size="74"
                        :md-stroke="3"
                        :md-progress="uploadProgress"></md-spinner>
                </div>
            </md-layout>
        </md-layout>
    </md-layout>
</template>

<style scoped>
h2,
h3 {
    width: 100%;
    min-width: 100%;
    margin-top: 0px;
}

.firstAuthorCard {
    margin-top: 7%;
}

/* .mainTab:not(.mobileMode) >>> nav {

} */

.mainTab >>> nav {
    position: fixed;
    width: 85%;
    background-color: white !important;
    top: 7%;
}

.subTabs >>> nav {
    position: relative;
    width: 100%;
    background-color: transparent;
}

.removePadding {
    padding: 0px !important;
}

.cardSeparator {
    margin-top: 2em;
}

.rightAlign {
    justify-content: flex-end;
}

.flexAround {
    justify-content: space-around;
}

.uploadContainer {
    position: relative;
}

.uploadSpinner {
    position: absolute;
    top: -3px;
    left: -1px;
}

.floatingAction {
    position: fixed !important;
    bottom: 16px !important;
    right: 16px !important;
}

.bottomSpace {
    margin-bottom: 5em;
}

.hidden {
        width: 0px;
        height: 0px;
        flex-grow: 0;
        flex-basis: 0%;
    }
</style>


<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import { ITopic, IQuestionBuilder, IQuestion, IDistractor } from "../../interfaces/models";
import { addEventsToQueue } from "../../util";
import TopicService from "../../services/TopicService";
import AuthorService from "../../services/AuthorService";
import ImageService from "../../services/ImageService";
import Fetcher from "../../services/Fetcher";
import tinyMCEPlugins from "./plugins";

import TinyMCE from "../util/TinyMCE.vue";
import TopicChip from "../util/TopicChip.vue";
import Question from "../questions/Question.vue";

@Component({
    components: {
        TinyMCE,
        Question,
        TopicChip
    }
})
export default class AuthorView extends Vue {

    pTopics: ITopic[] = [];
    @Prop question = p<IQuestionBuilder>({
        default: () => ({
            content: "",
            explanation: "",
            responses: {
                A: "",
                B: "",
                C: "",
                D: ""
            },
            correctIndex: "",
            topics: []
        })
    });
    @Prop id = p<number>({
        default: -1
    });

    uploadDone = false;
    correctQuestion = "";
    networkMessage = "";
    uploadProgress = 0;
    path = "/questions/add/";
    messageTitle = "Added Question";
    message = "Successfully added question";

    prevDisabled = true;
    prevLabel: string = "Please fill out all question fields to see preview";
    prevTooltip: string | undefined = "Please fill out all question fields to see preview.";
    pDisabled = false;

    bottomSpaceClass: string = "bottomSpace"

    mobileMode = false;

    get questionPrev():IQuestion | undefined {
        const error = AuthorService.validateQuestions(this.question);
        let qPrev: IQuestion | undefined;
        if (error === "") {
            let qSolution: IDistractor;

            const qDistractors: IDistractor[] = [
                {
                    id: -1,
                    content: this.question.responses["A"],
                    isCorrect: false,
                    response: "A"
                }, {
                    id: -2,
                    content: this.question.responses["B"],
                    isCorrect: false,
                    response: "B"
                }, {
                    id: -3,
                    content: this.question.responses["C"],
                    isCorrect: false,
                    response: "C"
                }, {
                    id: -4,
                    content: this.question.responses["D"],
                    isCorrect: false,
                    response: "D"
                }
            ];

            //qSolution = qDistractors[0];
            qSolution = {
                id: -5,
                content: "",
                isCorrect: true,
                response: ""
            };
            for (let d of qDistractors) {
                if (d.response == this.question.correctIndex) {
                    d.isCorrect=true;
                    qSolution = d;
                }
            }

            qPrev = {
                id: -1,
                difficulty: 0,
                quality: 0,
                topics: this.question.topics,
                content: this.question.content,
                explanation: this.question.explanation,
                solution: qSolution,
                distractors: qDistractors,
                responseCount: 0
            };
            this.prevDisabled = false;
            this.prevLabel = "Preview Question";
        } else {
            qPrev = undefined;
            this.prevDisabled = true;
            this.prevLabel = error;
        }
        return qPrev;
    }

    @Lifecycle
    created() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateTopics);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateTopics);
    }

    @Lifecycle
    mounted() {
        const visible = (this.$refs.onlyVisibleOnMobile as Vue);
        const isVisible = visible.$el;
        if (window.getComputedStyle(isVisible).display !== "none") {
            this.mobileMode = true;
        } else {
            this.mobileMode = false;
        }
    }

    get disabled() {
        return this.pDisabled;
    }

    set disabled(shouldHide: boolean) {
        this.pDisabled = shouldHide;
        const changeEditor = (mode: any) => {
            tinymce.get().forEach((editor: any) => {
                editor.setMode(mode);
            });
        };

        changeEditor(shouldHide ? "readonly" : "design");
    }

    toggleTopic(topicToToggle: ITopic) {
        const topicIndex = this.question.topics.indexOf(topicToToggle);
        if (topicIndex == -1) {
            this.question.topics.push(topicToToggle);
        } else {
            this.question.topics.splice(topicIndex, 1);
        }
    }

    topicIsUsed(topic: ITopic) {
        return this.question.topics.indexOf(topic) >= 0;
    }

    updateTopics(newTopics: ITopic[]) {
        this.pTopics = newTopics;
    }

    get topics() {
        return this.pTopics;
    }

    get options() {
        return {
            skin: false,
            image_caption: true,
            media_live_embeds: true,

            plugins: tinyMCEPlugins.plugins,
            toolbar: tinyMCEPlugins.toolbar,
            image_advtab: true,
            file_browser_callback_types: "image",
            file_picker_callback: ImageService.handleFileClick,
            file_picker_types: "image"
        };
    }

    navigateToAnswer() {
        this.$router.push("questions");
    }

    validateUpload() {
        const error = AuthorService.validateQuestions(this.question);

        if (error !== "") {
            addEventsToQueue([{
                name: "Invalid Question",
                description: error,
                icon: "error"
            }]);
        } else {
            this.disabled = true;
            if (this.id >= 0) {
                this.path = "/questions/update/"+this.id+"/";
                this.messageTitle = "Updated Question";
                this.message = "Successfully updated question";
            }
            AuthorService.prepareUpload(this.question)
                .then(preparedUpload => AuthorService.uploadContent(preparedUpload, this.path))
                .then(response => {
                    addEventsToQueue([{
                        name: this.messageTitle,
                        description: this.message,
                        icon: "done"
                    }]);
                    this.$router.push(`/question/id/${response.id}`);
                });
        }
    }

    tabSelected(index: number) {
        if (index==1) {
            this.bottomSpaceClass="";
        } else {
            this.bottomSpaceClass = "bottomSpace";
        }
    }

}

</script>
