<template>
    <textarea :id="id"></textarea>
</template>

<script lang="ts">
import { Vue, Component, Prop, p, Watch, Lifecycle } from "av-ts";

@Component
export default class TinyMCE extends Vue {
    @Prop id = p<string>({
        required: true
    });
    @Prop options = p<any>({
        required: false,
        default: () => {}
    });
    @Prop value = p<string | undefined>({
        required: false
    });

    @Prop version = p<number>({
        default: 0
    });

    @Watch("version")
    watchVersion(_n: number, _o: number) {
        tinymce.get(this.id).setContent(this.value);
    }

    @Watch("options")
    optionsChanged(_oldOptions: any, _newOptions: any) {
        tinymce.execCommand("mceRemoveEditor", false, this.id);
        this.createEditor();
    }

    createEditor() {
        let options: any = {};
        let config = (editor: any) => {
            editor.on("NodeChange Change KeyUp", (_e: any) => {
                this.$emit("input", tinymce.get(this.id).getContent());
                this.$emit("change", tinymce.get(this.id), tinymce.get(this.id).getContent());
            });

            editor.on("init", (_e: any) => {
                if (this.value != undefined) {
                    tinymce.get(this.id).setContent(this.value);
                }
            });
        };

        //Default configuration
        let s1 = (e: any) => config(e);
        if (typeof this.options == "object") {
            options = Object.assign({}, this.options);
            if (!this.options.hasOwnProperty("selector")) {
                options.selector = "#" + this.id;
            }

            if (typeof this.options.setup == "function") {
                s1 = editor => {
                    config(editor);
                    this.options.setup(editor);
                };
            }
        } else {
            options.selector = "#" + this.id;
        }

        options.setup = (editor: any) => s1(editor);
        this.$nextTick(() => tinymce.init(options));
    }

    @Lifecycle
    mounted() {
        this.createEditor();
    }

    @Lifecycle
    beforeDestroy() {
        tinymce.execCommand("mceRemoveEditor", false, this.id);
    }
}
</script>
