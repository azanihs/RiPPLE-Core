<template>
<md-card class="recommendationCard">
    <md-card-header>
        <md-avatar>
            <img :src="data.image" :alt="data.name">
        </md-avatar>
        <md-card-expand>
            <md-card-actions>
                <span>{{ data.name }}</span>
                <span style="flex: 1"></span>
                <md-button class="md-icon-button" md-expand-trigger>
                    <md-icon>keyboard_arrow_down</md-icon>
                </md-button>
            </md-card-actions>
            <md-card-content>
                "{{ data.bio }}"
            </md-card-content>
        </md-card-expand>
    </md-card-header>
    <md-card-area>
        <md-card-content>
            <div class="card-reservation">
                <md-button-toggle md-single class="md-button-group">
                    <md-button v-for="time in data.availableTimes" :key="time"> {{ time }}</md-button>
                </md-button-toggle>
                <span>
                    <router-link v-for="prof in data.proficiencies" :key="prof" to="/view/peers" class="topicChipLink">
                        <md-chip class="topicChip">{{ prof }}</md-chip>
                    </router-link>
                </span>
            </div>
        </md-card-content>
    </md-card-area>
    <md-card-actions>
        <md-button class="md-primary">ignore</md-button>
        <md-button class="md-primary">{{ action }}</md-button>
    </md-card-actions>
</md-card>
</template>

<style scoped>
    .recommendationCard a.topicChipLink,
    .recommendationCard a.topicChipLink:visited {
        color: #333;
        text-decoration: none;
        transition: 500ms ease background-color, 500ms ease color;
    }
    .recommendationCard a.topicChipLink:hover {
        color: #bbb;
        text-decoration: none;
    }
    .recommendationCard .topicChip {
        margin-left: 5px;
        background-color: #fff;
        border: 1px solid #ccc;
        transition: 500ms ease background-color;
    }
    .topicChip:hover {
        background-color: #333;
    }
</style>

<script lang="ts">
    import { Vue, Component, Prop } from "av-ts";

    @Component()
    export default class RecommendationCard extends Vue {
        @Prop data;
        @Prop action: string;
    }
</script>
