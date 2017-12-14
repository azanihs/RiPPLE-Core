<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100">
            <md-card v-if="consentForm" class="heading">
                <h2>Edit consent form for {{ pCourseCode }}</h2>
                <p v-if="hasPrevAuthor">Last edited by: {{ pPreviousAuthor }}</p>
                <TinyMCE id="consentEditor"
                    v-model="consentForm.text"
                    :options="options"></TinyMCE>
            </md-card>
        </md-layout>
        <md-layout md-flex="100"
            class="rightAlign">
            <div class="uploadContainer cardSeparator">
                <md-tooltip
                    md-direction="left">Upload Consent Form</md-tooltip>
                <md-button class="md-fab md-raised uploadButton"
                    @click="validateUpload">
                    <md-icon>cloud_upload</md-icon>
                </md-button>
            </div>
        </md-layout>
    </md-layout>
</template>

<style scoped>
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
import { ICourseUser, IConsentForm } from "../../interfaces/models";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";
import ImageService from "../../services/ImageService";
import TinyMCE from "../util/TinyMCE.vue";
import tinyMCEPlugins from "../author/plugins";
import { addEventsToQueue } from "../../util";

@Component({
    components: {
        TinyMCE
    }
})
export default class ConsentView extends Vue {
    pCourseCode = "";

    pCourseUser: ICourseUser | undefined = undefined;
    pPreviousAuthor: string | undefined = undefined;

    pConsentForm: IConsentForm | undefined = undefined;

    uploadDone = false;
    pDisabled = false;

    updateCourseUser(user: ICourseUser) {
        if (user.roles.indexOf("Instructor") == -1) {
            this.$router.push("../error/403");
        }

        this.pCourseCode = user.course.courseCode;
        this.pCourseUser = user;
    }

    setConsentForm(consentForm: IConsentForm | undefined) {
        if (consentForm !== undefined && consentForm.text) {
            this.pPreviousAuthor = consentForm.author.user.name;
            this.pConsentForm = consentForm;
        } else {
            this.pConsentForm = {
                text: "",
                author: this.pCourseUser!
            };
        }
    }

    get hasConsentForm() {
        return this.pConsentForm && this.pConsentForm.text !== undefined;
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
            file_picker_types: "image"
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
                .then(preparedUpload => UserService.uploadContent(preparedUpload));
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
}
</script>
