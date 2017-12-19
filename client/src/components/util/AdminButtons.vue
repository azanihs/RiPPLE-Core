<template>
    <md-layout class="buttonContainer">
        <responsive-wrapper>
            <div class="fixedButtons">
            <action-buttons>
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
                    v-if="questionExists"
                    class="md-warn"
                    slot="right"
                    @click="deleteQuestion">
                    <span>Delete Question</span>
                </md-button>
            </action-buttons>
            </div>
        </responsive-wrapper>
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
    width: 100%;
}

.fixedButtons >>> .right {
    justify-content: center !important;
}

.mobileStyle >>> .right {
    justify-content: space-between !important;
}

.mobileStyle > .fixedButtons {
    position: relative !important;
    background-color: transparent !important;
}

</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import ActionButtons from "./ActionButtons.vue";
import ResponsiveWrapper from "../util/ResponsiveWrapper.vue";

@Component({
    components: {
        ActionButtons,
        ResponsiveWrapper
    }
})

export default class AdminButtons extends Vue {
    @Prop showEdit = p<boolean>({
        required: true
    });

    @Prop questionExists = p<boolean>({
        default: false
    });

    saveQuestion() {
        this.$emit("saveQuestion");
    }

    deleteQuestion() {
        this.$emit("deleteQuestion");
    }

    editQuestion() {
        this.$emit("editQuestion");
    }
}
</script>
