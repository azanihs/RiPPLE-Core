<template>
<md-card >
    <md-card-header>
        <md-avatar>
            <img :src="data.image" :alt="data.name">
        </md-avatar>
        <md-card-expand>
            <md-card-actions>
                <md-button>{{ data.name }}</md-button>
                <span style="flex: 1"></span>
                <md-button class="md-icon-button" md-expand-trigger>
                    <md-icon>keyboard_arrow_down</md-icon>
                </md-button>
            </md-card-actions>
            <md-card-content>
                {{ data.bio }}
            </md-card-content>
        </md-card-expand>
    </md-card-header>
    <md-card-area>
        <md-card-content>
            <div class="card-reservation">
                <md-button-toggle md-single class="md-button-group">
                    <md-button> {{ data.time }}</md-button>
                </md-button-toggle>
                <span>
                    <md-chip v-for="prof in data.proficiencies" :key="prof" class="topicChip">{{prof}}</md-chip>
                </span>
            </div>
        </md-card-content>
    </md-card-area>
    <md-card-actions>
        <md-button class="md-primary">ignore</md-button>
        <md-button class="md-primary">Send Request</md-button>
    </md-card-actions>
</md-card>
</template>

<style scoped>
</style>

<script lang="ts">
    import { Vue, Component, Prop } from "av-ts";

    @Component()
    export default class RecommendationCard extends Vue {
        @Prop data;
    }
</script>
