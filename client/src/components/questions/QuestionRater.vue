<template>
    <div>
        <h2>
            <slot></slot>
        </h2>
        <rating :max="5"
                @input="rateAction"
                :disabled="disabled"
                :icon="icon"
                :defaultIndex="defaultValue"></rating>
    </div>
</template>

<style scoped>
h2 {
    padding: 0px;
    margin: 0px;
    color: #222;
    font-size: 0.8em;
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
    @Prop rateAction = p({
        type: Function
    });
}

</script>
