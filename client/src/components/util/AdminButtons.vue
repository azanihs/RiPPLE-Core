<template>
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
            v-if="canSave"
            class="primary-colour"
            slot="centreRight"
            @click="saveQuestion">
            <span>Save Question</span>
        </md-button>
        <md-button
            v-if="canEdit"
            class="primary-colour"
            slot="centreRight"
            @click="editQuestion">
            <span>Edit Question</span>
        </md-button>
        <md-button
            class="md-warn"
            slot="right"
            @click="deleteQuestion">
            <span>Delete Question</span>
        </md-button>
    </action-buttons>
</template>

<style scoped>
.primary-colour {
    color:#256
}

.prev-versions {
    flex-grow: 1;
    flex: unset;
    width: unset;
}
</style>

<script lang="ts">
import { Vue, Component, Watch, Prop, p } from "av-ts";
import ActionButtons from "./ActionButtons.vue";
import { addEventsToQueue } from "../../util";
import QuestionService from "../../services/QuestionService";
import { IQuestion } from "../../interfaces/models";

@Component({
    components: {
        ActionButtons
    }
})

export default class AdminButtons extends Vue {
    @Prop id = p<number>({
        required: true
    });

    @Prop canEdit = p<boolean>({
        default: false
    });

    @Prop canSave = p<boolean>({
        default: false
    });

    @Prop prevQuestions = p<IQuestion[]>({});


    pVersion: number = 0;

    get version() {
        return this.pVersion;
    }

    set version(newVersion: number) {
        this.pVersion = newVersion;
    }
    saveQuestion() {
        this.$emit("saveQuestion");
    }

    editQuestion() {
        this.$router.push(`/question/edit/`+this.id);
    }

    deleteQuestion() {
        QuestionService.deleteQuestion(this.id)
            .then(() => {
                addEventsToQueue([{
                    id: -7,
                    name: "Question Deleted",
                    description: "Successfully deleted question",
                    icon: "done"
                }]);
            })
            .then(() => {
                this.$router.go(-1);
            });
    }

    @Watch("version")
    versionWatch(_newValue: number, _oldValue: number) {
        this.$emit("version", this.version);
    }
}
</script>
