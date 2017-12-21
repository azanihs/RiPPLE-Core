<template>
    <md-layout class="buttonContainer">
        <div class="fixedButtons"
        :class = "{'mobileStyle': mobileMode}">
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

</style>

<script lang="ts">
import { Vue, Lifecycle, Component, Prop, p } from "av-ts";
import ActionButtons from "./ActionButtons.vue";
import ApplicationService from "../../services/ApplicationService";

@Component({
    components: {
        ActionButtons
    }
})

export default class AdminButtons extends Vue {
    @Prop showEdit = p<boolean>({
        required: true
    });

    @Prop questionExists = p<boolean>({
        default: false
    });

    mobileMode:boolean = false;

    @Lifecycle
    mounted() {
        this.mobileMode = ApplicationService.getMobileMode();
        console.log(this.mobileMode);
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
}
</script>
