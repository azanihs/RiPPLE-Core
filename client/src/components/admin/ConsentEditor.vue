<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100">
            <md-card v-if="consentForm" class="heading">
                <md-tabs md-fixed class="md-transparent">
                    <md-tab id="edit_tab" md-label="Edit">
                        <h2>Edit consent form for {{ courseCode }}</h2>
                        <p v-if="hasPrevAuthor">Last edited by: {{ pPreviousAuthor }}</p>
                        <p class="warn" v-if="oldConsentFormContent === ''">Your course does not have a consent form active</p>
                        <p class="warn" v-else-if="hasUnsavedChanges">You have unsaved changes</p>
                        <TinyMCE id="consentEditor"
                            v-model="consentForm.content"
                            :options="options"></TinyMCE>
                        <md-layout md-flex="100"
                            class="rightAlign">
                            <div class="uploadContainer cardSeparator">
                                <md-tooltip md-direction="left">Upload Consent Form</md-tooltip>
                                <md-button class="md-fab md-raised uploadButton"
                                    @click="validateUpload">
                                    <md-icon>cloud_upload</md-icon>
                                </md-button>
                            </div>
                        </md-layout>
                    </md-tab>
                    <md-tab id="preview_tab" md-label="Preview">
                        <consent-form :consentForm="consentForm" :courseCode="courseCode" :response="undefined"></consent-form>
                    </md-tab>
                </md-tabs>
            </md-card>
        </md-layout>
    </md-layout>
</template>

<style scoped>
.warn {
    color: red
}
.heading {
    flex-direction: column;
}
.md-fab {
    margin-left: auto;
}

.rightAlign {
    justify-content: flex-end;
}

</style>

<script lang="ts">
import { Vue, Component, Lifecycle } from "av-ts";
import { CourseUser, IConsentForm } from "../../interfaces/models";

import { getDefaultConsentForm } from "../../util";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";
import ImageService from "../../services/ImageService";

import tinyMCEPlugins from "../author/plugins";
import { addEventsToQueue } from "../../util";

import TinyMCE from "../util/TinyMCE.vue";
import ConsentForm from "../profile/ConsentForm.vue";

@Component({
    components: {
        TinyMCE,
        ConsentForm
    }
})
export default class ConsentEditor extends Vue {
    pCourseCode = "";

    pCourseUser: CourseUser | undefined = undefined;
    pPreviousAuthor: string | undefined = undefined;

    pConsentForm: IConsentForm | undefined = undefined;

    pOldConsentFormContent: string = "";

    uploadDone = false;
    pDisabled = false;

    updateCourseUser(user: CourseUser) {
        if (user.roles.indexOf("Instructor") == -1) {
            this.$router.push("../error/403");
        }

        this.pCourseCode = user.course.courseCode;
        this.pCourseUser = user;
    }

    setConsentForm(consentForm: IConsentForm | undefined) {
        if (consentForm !== undefined && consentForm.content) {
            this.pPreviousAuthor = consentForm.author.user.name;
            this.pConsentForm = consentForm;
            this.pOldConsentFormContent = consentForm.content;
        } else {
            this.pConsentForm = {
                content: getDefaultConsentForm(),
                author: this.pCourseUser!
            };
        }
    }

    get oldConsentFormContent() {
        return this.pOldConsentFormContent;
    }

    get hasUnsavedChanges() {
        if (this.pConsentForm) {
            return this.pOldConsentFormContent.trim() !== this.pConsentForm.content.trim();
        } else {
            return false;
        }
    }

    get hasConsentForm() {
        return this.pConsentForm && this.pConsentForm.content !== undefined;
    }

    get hasPrevAuthor() {
        return this.pPreviousAuthor !== undefined;
    }

    get consentForm() {
        return this.pConsentForm;
    }

    set consentForm(newConsentForm: IConsentForm | undefined) {
        this.pConsentForm = newConsentForm;
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
            file_picker_types: "image",
            height: 480
        };
    }

    validateUpload() {
        const error = UserService.validateConsentForm(this.consentForm!);

        if (error !== "") {
            addEventsToQueue([{
                id: -5,
                name: "Invalid Consent Form",
                description: error,
                icon: "error"
            }]);
        } else {
            this.disabled = true;
            UserService.prepareConsentUpload(this.consentForm!)
                .then(preparedUpload => UserService.uploadContent(preparedUpload))
                .catch(err => {
                    addEventsToQueue([{
                        id: -6,
                        name: "Consent Form",
                        description: err,
                        icon: "error"
                    }]);
                })
                .then(() => {
                    this.disabled = false;
                    this.pOldConsentFormContent = this.consentForm!.content;
                    addEventsToQueue([{
                        id: -6,
                        name: "Consent Form",
                        description: "Consent Form Saved",
                        icon: "done"
                    }]);
                });
        }
    }

    @Lifecycle
    created() {
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateCourseUser);
        Fetcher.get(UserService.getConsentForm)
            .on(this.setConsentForm);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateCourseUser);
        Fetcher.get(UserService.getConsentForm)
            .off(this.setConsentForm);
    }

    get courseCode() {
        return this.pCourseCode;
    }
}
</script>
