<template>
<md-layout>
    <md-layout>
        <h2><md-icon>school</md-icon>  Select topics that you would like to {{ tabName }}</h2>
        <md-layout md-flex="100" md-column class="positionRelative">
            <div v-if="+threshold > 0" class="thresholdWrapper" v-bind:style="{marginLeft: threshold + '%'}">
                <md-tooltip md-direction="top">Required Score To Mentor: {{ threshold }}</md-tooltip>
            </div>
            <md-layout v-for="(topicScore, topicName) in topics" @click.native="selectTopic(topicName)" class="alignMiddle mentorshipWrapper" v-bind:class="{selected: selectedTopics.indexOf(topicName) >= 0, fade: +topicScore < +threshold}" :key="topicName">
                <md-layout>{{ topicName }}</md-layout>
                <md-layout md-flex="95">
                    <md-progress :md-progress="topicScore"></md-progress>
                </md-layout>
            </md-layout>
        </md-layout>
    </md-layout>
    <md-layout md-flex="100">
        <h2><md-icon>people</md-icon> Review recommendations</h2>
        <md-layout md-flex="100">
            <md-layout v-for="peer in peers.recommendations" :key="peer.id">
                <recommendation-card class="gutter" :data="peer" action="Request"/>
            </md-layout>
        </md-layout>
    </md-layout>
    <md-layout md-flex="100">
        <h2><md-icon>person_add</md-icon> Respond to requests</h2>
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
.thresholdWrapper {
    cursor: pointer;
    width: 5px;
    height: 100%;
    background-color: #ccc;
    position: absolute;
    left: 0px;
    top: 0px;
    z-index: 1000;
}
.positionRelative {
    position: relative;
}
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

