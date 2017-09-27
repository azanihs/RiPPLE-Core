<template>
    <p>
        Empty author page
        <tinymce id="editor"
                 v-model="editor"
                 :options="options"
                 @change="change"
                 :content="''"></tinymce>
    </p>
</template>

<style>

</style>


<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { Topic } from "../../interfaces/models";
import TopicService from "../../services/TopicService";
import Fetcher from "../../services/Fetcher";
import tinyMCEPlugins from "./plugins";


@Component()
export default class AuthorView extends Vue {

    pTopics: Topic[] = [];
    editor = "";

    change() {

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
