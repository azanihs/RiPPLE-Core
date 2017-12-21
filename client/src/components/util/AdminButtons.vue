<template>
    <md-layout class="buttonContainer">
        <div class="fixedButtons"
        :class = "{'mobileStyle': mobileMode}">
        <action-buttons>
            <md-input-container v-if="prevQuestions" class="prev-versions"
                slot="centreLeft" style="min-width:200px">
                <label for="prevQuestions">Version:</label>
                <md-select
                    name="prevQuestions"
                    id="prevQuestions"
                    v-model="version"
                    md-change="versionChanged()">
                    <md-option :value="0">
                        Version: Current
                    </md-option>
                    <md-option v-for="i in prevQuestions.length" :key="i" :value="i">
                        Version {{ prevQuestions.length - i + 1 }}: {{ prevQuestions[i-1]["createdAt"] }}
                    </md-option>
                </md-select>
            </md-input-container>
            <md-button
                v-if="showEdit"
                class="primary-colour"
                slot="centreRight"
                @click="editQuestion">
                <span>Edit Question</span>
            </md-button>
            <md-button
                v-else
                class="primary-colour"
                slot="centreRight"
                @click="saveQuestion">
                <span>Save Question</span>
            </md-button>
            <md-button
                v-if="id"
                class="md-warn"
                slot="right"
                @click="deleteQuestion">
                <span>Delete Question</span>
            </md-button>
        </action-buttons>
        </div>
    </md-layout>
</template>

<style scoped>
.primary-colour {
    color:#256
}
.buttonContainer {
    width: 100%;
    justify-content: space-between;
    margin-bottom: 0.5;
    flex: unset;
}

.fixedButtons{
    position: fixed;
    background-color: white;
    z-index: 100;
    width: 83.75%;
    left: 16.25%;
    top: 0px;
}

.fixedButtons .right {
    justify-content: center !important;
}

.mobileStyle .right {
    justify-content: space-between !important;
}

.mobileStyle.fixedButtons {
    position: relative !important;
    background-color: transparent !important;
    width: 100% !important;
    left: 0px;
}

.prev-versions {
    flex-grow: 1;
    flex: unset;
    width: unset;
    margin: 0px;
}

</style>

<script lang="ts">
import { Vue, Lifecycle, Watch, Component, Prop, p } from "av-ts";
import ActionButtons from "./ActionButtons.vue";
import ApplicationService from "../../services/ApplicationService";
import { IQuestionBuilder } from "../../interfaces/models";

@Component({
    components: {
        ActionButtons
    }
})

export default class AdminButtons extends Vue {
    @Prop showEdit = p<boolean>({
        required: true
    });

    @Prop id = p<number>({});

    @Prop prevQuestions = p<IQuestionBuilder[]>({});

    pVersion: number = 0;

    mobileMode:boolean = false;

    get version() {
        return this.pVersion;
    }
    set version(newVersion: number) {
        this.pVersion = newVersion;
    }

    @Lifecycle
    mounted() {
        this.mobileMode = ApplicationService.getMobileMode();
    }

    saveQuestion() {
        this.$emit("saveQuestion");
    }

    deleteQuestion() {
        this.$emit("deleteQuestion");
    }

    editQuestion() {
        this.$emit("editQuestion");
    }

    @Watch("version")
    versionWatch(_newValue: number, _oldValue: number) {
        this.$emit("version", this.version);
    }
}
</script>
