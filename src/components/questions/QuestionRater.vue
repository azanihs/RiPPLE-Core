<template>
    <md-card class="card"
             md-with-hover>
        <md-card-header class="cardHeader">
            <md-card-header-text>
                <div class="md-title">
                    <slot></slot>
                </div>
            </md-card-header-text>
    
            <md-card-media class="cardIcon">
                <md-icon>{{icon}}</md-icon>
            </md-card-media>
        </md-card-header>
    
        <md-card-actions class="cardAction">
            <rating :max="5"
                    :disabled="disabled"
                    :icon="icon"
                    :defaultIndex="defaultValue"></rating>
        </md-card-actions>
    </md-card>
</template>

<style scoped>
    .card {
        position: relative;
        width: 100%;
        background-color: transparent !important;
    }
    
    .card:not(:first-of-type) {
        margin-top: 2em;
    }
    
    .cardIcon {
        text-align: right;
        height: auto !important;
    }
    
    .cardHeader {
        align-items: center;
    }
    
    .md-title {
        margin-top: 0px !important;
    }
    
    .cardAction {
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
