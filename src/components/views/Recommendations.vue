<template>
<md-layout>
    <md-layout>
        <h2><md-icon>school</md-icon> {{ tabName }}</h2>
        <md-layout md-flex="100" md-column>
            <md-layout v-for="(topicScore, topicName) in topics" @click.native="selectTopic(topicName)" class="alignMiddle mentorshipWrapper" v-bind:class="{selected: selectedTopics.indexOf(topicName) >= 0, fade: +topicScore < +threshold}">
                <md-layout>{{ topicName }}</md-layout>
                <md-layout md-flex="95">
                    <md-progress :md-progress="topicScore"></md-progress>
                </md-layout>
            </md-layout>
        </md-layout>
    </md-layout>
    <md-layout md-flex="100">
        <h2><md-icon>people</md-icon> Recommendations</h2>
        <md-layout md-flex="100">
            <md-layout v-for="peer in peers.recommendations" :key="peer.id">
                <recommendation-card class="gutter" :data="peer" action="Request"/>
            </md-layout>
        </md-layout>
    </md-layout>
    <md-layout md-flex="100">
        <h2><md-icon>person_add</md-icon> Requests</h2>
        <md-layout md-flex="100">
            <md-layout v-for="peer in peers.requests" :key="peer.id">
                <recommendation-card class="gutter" :data="peer" action="Accept" />
            </md-layout>
        </md-layout>
    </md-layout>
</md-layout>
</template>
<style>
    .mentorshipWrapper {
        cursor: pointer;
        transition: background 500ms ease;
    }
    .mentorshipWrapper:hover:not(.fade) {
        background-color: #fafafa;
    }
    .mentorshipWrapper:hover:not(.fade) .md-progress-track {
        background-color: #ff5722 !important;
    }

    .mentorshipWrapper.selected .md-progress-track {
        background-color: #ff5722 !important;
    }
    .mentorshipWrapper.selected {
        background-color: #fafafa;
    }

    .mentorshipWrapper.fade {
        opacity: 0.5;
    }

    .fade .mentorshipWrapper .md-progress-track {
        background-color: transparent !important;
    }
</style>

<style scoped>
.gutter {
    margin: 8px;
}
.proficiencyWrapper {
    display: block;
    width: 100%;
}
.alignMiddle {
    align-items: center;
}
</style>

<script lang="ts">
    import { Vue, Component, Prop } from "av-ts";
    import RecommendationCard from "./RecommendationCard";

    @Component({
        components: {
            "recommendation-card": RecommendationCard
        }
    })
    export default class Recommendations extends Vue {
        @Prop peers;
        @Prop tabName: string;
        @Prop threshold: number;

        topics = {
            "SSL": Math.random() * 100,
            "CSS": Math.random() * 100,
            "JSON": Math.random() * 100,
            "RSS": Math.random() * 100,
            "AI": Math.random() * 100,
            "XML": Math.random() * 100
        };
        selectedTopics = [];

        selectTopic(topicName) {
            const topicIndex = this.selectedTopics.indexOf(topicName);
            if (!this.topics[topicName] || +this.topics[topicName] < +this.threshold) {
                return;
            }

            if (topicIndex < 0) {
                this.selectedTopics.push(topicName);
            } else {
                this.selectedTopics.splice(topicIndex, 1);
            }

            this.$emit("change");
        }
    }
</script>

