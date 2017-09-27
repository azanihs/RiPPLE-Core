<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100">
            <h3>Question</h3>
            <tinymce id="questionEditor"
                     v-model="questionContent"
                     :options="options"
                     :content="''"></tinymce>
        </md-layout>
        <md-layout md-flex="100">
            <h3>Topics</h3>
            <topic-chip v-for="topic in topics"
                        :key="topic.id"
                        :disabled="!topicIsUsed(topic)"
                        @click.native="toggleTopic(topic)">
                {{topic.name}}
            </topic-chip>
        </md-layout>
        <md-layout md-flex="100"
                   v-for="i in ['A', 'B', 'C', 'D']"
                   :key="i">
            <h3>Response {{i}}</h3>
            <tinymce :id="'editor_' + i"
                     v-model="questionResponses[i]"
                     :options="options"
                     :content="''"></tinymce>
        </md-layout>

        <div class="uploadContainer">
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
</template>

<style scoped>
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
    questionResponses = [];

    questionTopics = [];
    uploadDone = false;
    uploadProgress = 0;

    validateUpload() {
        setInterval(() => {
            this.uploadProgress += 1;
            if (this.uploadProgress >= 100) {
                this.uploadDone = true;
            }
        }, 100);
    }

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
            file_browser_callback_types: "file image media",
            file_picker_callback: function(resolve, currentFieldValue, fieldMeta) {
                console.log(fieldMeta);
                const image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAAnElEQ"
                    + "VR42u3RAQ0AAAgDoJvc6FrDOahAZdLhjBIiBCFCECIEIUIQIkSIEIQIQYgQhAhBiBCEIEQIQoQgRAhChCAEI"
                    + "UIQIgQhQhAiBCEIEYIQIQgRghAhCEGIEIQIQYgQhAhBCEKEIEQIQoQgRAhCECIEIUIQIgQhQhCCECEIEYIQI"
                    + "QgRghCECEGIEIQIQYgQhAgRIgQhQhAiBCHfLWUmlZ1jOmbgAAAAAElFTkSuQmCC";
                const file = undefined;

                Object.assign(fieldMeta, {
                    src: image,
                    href: image,
                    alt: "Green Box",
                    text: "Green Box",
                    title: "image.jpg"
                });

                resolve(file, fieldMeta);
            }
        };
    }
}
</script>
