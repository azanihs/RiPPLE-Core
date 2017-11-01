<template>
    <md-card class="commentCard">
        <md-card-header>
            <md-avatar>
                <img :src="comment.author.image"
                     :alt="comment.author.name">
            </md-avatar>
            <div class="md-title">{{comment.author.name}}</div>
            <div class="cardActions">
                <md-button class="upvote">
                    <span>{{comment.upVotes}}</span>
                    <md-icon>thumb_up</md-icon>
                </md-button>
            </div>
        </md-card-header>

        <md-card-content>
            {{comment.content}}
        </md-card-content>
    </md-card>
</template>

<style scoped>
.commentCard {
    width: 100%;
    margin-bottom: 16px;
}

.upvote span,
.upvote i {
    display: inline-block;
    vertical-align: middle;
    width: auto;
    height: auto;
    min-width: auto;
    min-height: auto;
    font-size: 16px;
}

.upvote span {
    font-size: 14px;
}

.cardActions {
    position: absolute;
    top: 16px;
    right: 16px;
    color: #256;
}
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { User, QuestionResponse } from "../../interfaces/models";

@Component()
export default class Comment extends Vue {
    @Prop comment = p({
        type: Object,
        required: true
    }) as QuestionResponse[];

}
</script>
