<template>
    <md-layout md-flex="100">
        <md-layout v-if="serverQuestionResponse" class="viewContainer">
            <md-layout md-flex="100" class="questionContainer">
                <question class="question"
                    :showSpeedDial="false"
                    @userAnswer="navigateToAnswer"
                    @newQuestion="navigateToAnswer"
                    :question="serverQuestionResponse"></question>
            </md-layout>
        </md-layout>
        <md-layout md-flex="100"
            v-if="serverQuestionResponse === undefined"
            class="cardSeparator">
            <md-card>
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
            v-if="serverQuestionResponse === undefined"
            class="cardSeparator">
            <md-card class="removePadding">
                <md-tabs md-fixed
                    :mdNavigation="false"
                    class="md-transparent tabContainer">
                    <md-tab v-for="i in ['A', 'B', 'C', 'D']"
                        :key="i"
                        :id="'tab_' + i"
                        :md-label="'Response ' + i">
                        <h3>Response {{i}}</h3>
                        <TinyMCE :id="'editor_' + i"
                            v-model="question.responses[i]"
                            :options="options"></TinyMCE>
                    </md-tab>
                </md-tabs>
            </md-card>
        </md-layout>
        <md-layout md-flex="100"
            v-if="serverQuestionResponse === undefined"
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
            v-if="serverQuestionResponse === undefined"
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
        <md-layout md-flex="100"
            v-if="serverQuestionResponse === undefined"
            class="rightAlign">
            <div class="uploadContainer cardSeparator">
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
</template>

<style scoped>
h2,
h3 {
    width: 100%;
    min-width: 100%;
    margin-top: 0px;
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

.uploadButton.done {
    background-color: #256 !important;
    color: #f2f2f2 !important;
}

.uploadContainer {
    position: relative;
}

.uploadSpinner {
    position: absolute;
    top: -3px;
    left: -1px;
}
</style>


<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { Question as QuestionModel, Topic, QuestionBuilder } from "../../interfaces/models";
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

    pTopics: Topic[] = [];
    question: QuestionBuilder = {
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
    };

    correctQuestion = "";
    networkMessage = "";
    uploadDone = false;
    uploadProgress = 0;

    pDisabled = false;
    serverQuestionResponse: QuestionModel | undefined = undefined;

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

    toggleTopic(topicToToggle: Topic) {
        const topicIndex = this.question.topics.indexOf(topicToToggle);
        if (topicIndex == -1) {
            this.question.topics.push(topicToToggle);
        } else {
            this.question.topics.splice(topicIndex, 1);
        }
    }

    topicIsUsed(topic: Topic) {
        return this.question.topics.indexOf(topic) >= 0;
    }

    updateTopics(newTopics: Topic[]) {
        this.pTopics = newTopics;
    }

    handleFileClick(resolve: any, _currentFieldValue: any, fieldMeta: any) {
        if (fieldMeta.filetype != "image") {
            return;
        }

        const input = document.createElement("input")!;
        input.type = "file";

        input.addEventListener("change", () => {
            const inputFiles = input.files!;
            if (inputFiles.length != 1) {
                return;
            }
            const file = inputFiles[0];
            ImageService.fileToBase64EncodeString(file)
                .then(x => {
                    // * tinyMCE will encode the uploaded image with an window.createObjectURL until it loses focus.
                    // ** It will use the base64 encoding when focus is lost.
                    // * When upload time happens, just pull all img srcs from the DOM object, and if they are not a base64 then encode the object to be so
                    resolve(x.base64, x._meta);
                })
                .catch(err => {
                    console.warn(err);
                });
        });

        // Dispatch a click event
        const clickEvent = new MouseEvent("click", {
            "view": window,
            "bubbles": true,
            "cancelable": true
        });
        input.dispatchEvent(clickEvent);
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
            file_picker_callback: this.handleFileClick,
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
                id: -1,
                name: "Invalid Question",
                description: error,
                icon: "error"
            }]);
        } else {
            this.disabled = true;
            AuthorService.prepareUpload(this.question)
                .then(preparedUpload => AuthorService.uploadContent(preparedUpload))
                .then(response => this.serverQuestionResponse = response);
        }
    }
}

</script>
