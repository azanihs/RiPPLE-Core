<template>
    <textarea :id="id"></textarea>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch, p, Lifecycle } from "av-ts";

declare const tinymce;
@Component
export default class TinyMCE extends Vue {
    @Prop id = p<string>({
        required: true
    });
    @Prop options = p<any>({
        required: false,
        default: () => {}
    });
    @Prop content = p<string | undefined>({
        required: false,
        default: ""
    });
    @Prop value = p<string | undefined>({
        required: false
    });


    @Watch("content")
    contentChanged() {
        tinymce.get(this.id).setContent(this.content);
    }

    @Lifecycle
    mounted() {
        //Initial configuration
        let options: any = {};
        let config = editor => {
            editor.on("NodeChange Change KeyUp", e => {
                this.$emit("input", tinymce.get(this.id).getContent());
                this.$emit("change", tinymce.get(this.id), tinymce.get(this.id).getContent());
            });

            editor.on("init", e => {
                if (this.content != undefined) {
                    tinymce.get(this.id).setContent(this.content);
                }

                this.$emit("input", this.content);
            });
        };

        //Default configuration
        let s1 = e => config(e);
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

        options.setup = editor => s1(editor);
        this.$nextTick(() => tinymce.init(options));
    }

    @Lifecycle
    beforeDestroy() {
        tinymce.execCommand("mceRemoveEditor", false, this.id);
    }

}
    /*export default {
        name: "tinymce",
        props: {
            id: {
                type: String,
                required: true
            },
            options: Object,
            content: {
                type: String,
                default: ''
            },
            value: String
        },
        watch: {
            content(){
                tinymce.get(this.id).setContent(this.content)
            }
        },
        mounted () {

            //Initial configuration
            let options = {}
            let s1 = new Function()
            let config = (editor) => {
                editor.on('NodeChange Change KeyUp', (e) => {
                    this.$emit('input', tinymce.get(this.id).getContent())
                    this.$emit('change', tinymce.get(this.id), tinymce.get(this.id).getContent())
                })
                editor.on('init', (e) => {
                    if(this.content != undefined) tinymce.get(this.id).setContent(this.content)
                    this.$emit('input', this.content)
                })
            }

            //Default configuration
            s1 = (e) => config(e)
            if(typeof this.options == 'object'){

                options = Object.assign({}, this.options)
                if(!this.options.hasOwnProperty('selector')) options.selector = '#' + this.id
                if(typeof this.options.setup == 'function'){
                    s1 = (editor) => {
                      config(editor)
                      this.options.setup(editor)
                    }
                }

            } else options.selector = '#' + this.id

            options.setup = (editor) => s1(editor);
            Vue.nextTick(() => tinymce.init(options))
        },
        beforeDestroy () {
            tinymce.execCommand('mceRemoveEditor', false, this.id)
        }
    }*/
</script>
