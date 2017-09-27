<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100"
                   class="cardSeparator">
            <md-card>
                <md-layout md-flex="100"
                           class="componentSeparator">
                    <h2>Question Body</h2>
                    <tinymce id="questionEditor"
                             v-model="questionContent"
                             :options="options"
                             :content="''"></tinymce>
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
                         class="md-transparent tabContainer">
                    <md-tab v-for="i in ['A', 'B', 'C', 'D']"
                            :key="i"
                            :id="'tab_' + i"
                            :md-label="'Response ' + i">
                        <h3>Response {{i}}</h3>
                        <tinymce :id="'editor_' + i"
                                 v-model="questionResponses[i]"
                                 :options="options"
                                 :content="''"></tinymce>
                        <md-radio v-model="correctQuestion"
                                  class="noBottomMargin"
                                  :md-value="i"
                                  name="correctQuestionGroup">Is Correct</md-radio>
                    </md-tab>
                </md-tabs>
            </md-card>
        </md-layout>
        <md-layout md-flex="100"
                   class="rightAlign">
            <div class="uploadContainer cardSeparator">
                <md-tooltip v-if="!uploadDone"
                            md-direction="top">Upload Question</md-tooltip>
                <md-tooltip v-if="uploadDone"
                            md-direction="top">Question Uploaded</md-tooltip>
                <md-button class="md-fab md-raised uploadButton"
                           @click="validateUpload"
                           :class="{'done': uploadDone}">
                    <md-icon v-if="!uploadDone">save</md-icon>
                    <md-icon v-if="uploadDone">done</md-icon>
                </md-button>
                <md-spinner class="progressSpinner uploadSpinner"
                            :md-size="74"
                            :md-stroke="3"
                            :md-progress="uploadProgress"></md-spinner>
            </div>
        </md-layout>

        <md-snackbar md-position="bottom center"
                     ref="snackbar"
                     md-duration="4000">
            <span>{{networkMessage}}</span>
            <md-button class="md-accent"
                       @click="$refs.snackbar.close()">Close</md-button>
        </md-snackbar>
    </md-layout>
</template>

<style scoped>
h2 {
    width: 100%;
    min-width: 100%;
    margin-top: 0px;
}

.removePadding {
    padding: 0px !important;
}

.cardSeparator {
    margin-top: 2em
}

.noBottomMargin {
    margin-bottom: 0px !important;
}

.rightAlign {
    justify-content: flex-end;
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
import { Topic } from "../../interfaces/models";
import TopicService from "../../services/TopicService";
import AuthorService from "../../services/AuthorService";

import Fetcher from "../../services/Fetcher";
import tinyMCEPlugins from "./plugins";

import TopicChip from "../util/TopicChip.vue";

@Component({
    components: {
        TopicChip
    }
})
export default class AuthorView extends Vue {

    pTopics: Topic[] = [];
    questionContent = "";
    questionResponses = {
        "A": "",
        "B": "",
        "C": "",
        "D": ""
    };
    correctQuestion = "";

    questionTopics = [];
    networkMessage = "";
    uploadDone = false;
    uploadProgress = 0;

    imageToBlobMap: Map<string, string> = new Map();

    toggleTopic(topicToToggle) {
        const topicIndex = this.questionTopics.indexOf(topicToToggle);
        if (topicIndex == -1) {
            this.questionTopics.push(topicToToggle);
        } else {
            this.questionTopics.splice(topicIndex, 1);
        }
    }

    topicIsUsed(topic) {
        return this.questionTopics.indexOf(topic) >= 0;
    }

    updateTopics(newTopics: Topic[]) {
        this.pTopics = newTopics;
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


    handleFileClick(resolve, currentFieldValue, fieldMeta) {
        if (fieldMeta.filetype != "image") {
            return;
        }

        const input = document.createElement("input");
        input.type = "file";

        input.addEventListener("change", () => {
            if (input.files.length != 1) {
                return;
            }
            const file = input.files[0];
            AuthorService.fileToBase64EncodeString(file)
                .then(x => {
                    // * tinyMCE will encode the uploaded image with an window.createObjectURL until it loses focus.
                    // ** It will use the base64 encoding when focus is lost.
                    // * When upload time happens, just pull all img srcs from the DOM object, and if they are not a base64 then encode the object to be so
                    resolve(x["base64"], x["_meta"]);
                })
                .catch(err => {
                    console.log(err);
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

    getBody(html) {
        const domParser = new DOMParser();
        const questionDOM = domParser.parseFromString(html, "text/html");
        return questionDOM.querySelector("body").innerHTML.trim();
    }

    validateQuestion(questionDOM) {
        const questionBody = this.getBody(questionDOM);

        return questionBody.length > 0;
    }

    validateUpload() {
        let error = "";
        const validator = {
            "Question cannot be empty": {
                validateFunction: this.validateQuestion,
                args: this.questionContent
            },
            "Question response 'A' cannot be empty": {
                validateFunction: this.validateQuestion,
                args: this.questionResponses.A
            },
            "Question response 'B' cannot be empty": {
                validateFunction: this.validateQuestion,
                args: this.questionResponses.B
            },
            "Question response 'C' cannot be empty": {
                validateFunction: this.validateQuestion,
                args: this.questionResponses.C
            },
            "Question response 'D' cannot be empty": {
                validateFunction: this.validateQuestion,
                args: this.questionResponses.D
            },
            "You must select which question is correct": {
                validateFunction: x => this.correctQuestion !== "",
                args: ""
            }
        };

        for (let errorMessage in validator) {
            if (validator[errorMessage] !== undefined) {
                const args = validator[errorMessage].args;
                if (validator[errorMessage].validateFunction(args) === false) {
                    error = errorMessage;
                    break;
                }
            }
        }

        if (error !== "") {
            this.networkMessage = error;
            (this.$refs.snackbar as any).open();
        } else {
            setInterval(() => {
                this.uploadProgress += 1;
                if (this.uploadProgress >= 100) {
                    this.uploadDone = true;
                }
            }, 100);
        }
    }
}
</script>
