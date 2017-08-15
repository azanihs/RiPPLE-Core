<template>
    <md-card>
        <md-card-header class="cardHeader">
            <md-card-header-text>
                <h2>
                    <slot></slot>
                </h2>
            </md-card-header-text>
        </md-card-header>
        <md-card-actions class="cardAction">
            <rating :max="10"
                    :disabled="disabled"
                    :icon="icon"
                    :defaultIndex="defaultValue"></rating>
        </md-card-actions>
    </md-card>
</template>

<style scoped>
.cardHeader {
    padding: 0px !important;
}

.cardIcon {
    text-align: right;
    height: auto !important;
}

h2 {
    padding: 0px;
    margin: 0px 0px 0.5em 0px;
    color: #666;
}

.cardAction {
    min-width: 100%;
    padding: 0px !important;
    justify-content: flex-start !important;
}
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";

import Rating from "./Rating.vue";

@Component({
    components: {
        Rating
    }
})
export default class QuestionRater extends Vue {
    @Prop icon = p({
        type: String,
        default: "star"
    });
    @Prop disabled = p({
        type: Boolean,
        default: false
    });
    @Prop defaultValue = p({
        type: Number,
        default: 0
    });
}

</script>
