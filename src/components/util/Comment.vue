<template>
    <md-layout md-gutter>
        <md-card>
            <md-card-header>
                <md-avatar>
                    <img :src="comment.author.image"
                         :alt="comment.author.name">
                </md-avatar>
    
                <div class="md-title">{{comment.author.name}}</div>
                <div class="md-subhead">{{String.fromCharCode('A'.charCodeAt(0) + comment.solution)}}</div>
    
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
    </md-layout>
</template>

<style scoped>
    .cardActions {
        position: absolute;
        top: 16px;
        right: 16px;
        display: flex;
        align-items: center;
    }
</style>

<script lang="ts">
    import { Vue, Component, Prop, p } from "av-ts";
    import { Peer } from "../../interfaces/models";

    @Component()
    export default class Comment extends Vue {
        @Prop comment = p({
            type: Object,
            required: true
        }) as {
            author: Peer,
            upVotes: number,
            content: string
        }

    }
</script>
