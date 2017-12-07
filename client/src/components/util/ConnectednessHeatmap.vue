<template>
    <md-card>
        <md-layout>
            <h2>Social Connectedness</h2>
            <table class="connectedTable">
                <thead>
                    <tr>
                        <th>Connection Type</th>
                        <th v-for="topic in topics"
                            :key="topic.id">
                            {{topic.name}}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="mentorType in categories"
                        :key="mentorType">
                        <td>{{mentorType}}</td>
                        <td v-for="topic in topics"
                            :key="topic.id"
                            :style="renderColor(mentorType, topic.id)">
                            {{renderWeights[mentorType][topic.id] || 0}}
                        </td>
                    </tr>
                </tbody>
            </table>
        </md-layout>
    </md-card>
</template>

<style scoped>
.connectedTable {
    table-layout: fixed;
    border-collapse: collapse;
    width: 100%;
}

h2 {
    margin-top: 0px;
}

.connectedTable th,
.connectedTable td {
    color: #444;
}

.connectedTable th {
    font-weight: 700;
    padding: 0.25em;
}

.connectedTable tr td:first-child {
    font-weight: 700;
}

.connectedTable td {
    padding: 0.25em;
}

.connectedTable td,
.connectedTable th {
    text-align: center;
    border: 1px solid #e0e0e0;
}

tr:hover td:first-child {
    background-color: transparent !important;
}

td:not(:first-child) {
    color: transparent !important;
    text-align: center;
}

td:hover {
    background-color: #eee !important;
    cursor: pointer;
    color: #222 !important;
}
</style>

<script lang="ts">
import { Vue, Prop, p, Lifecycle, Component, Watch } from "av-ts";

import { ITopic, IUser } from "../../interfaces/models";

import Fetcher from "../../services/Fetcher";
import UserService from "../../services/UserService";

interface IRenderWeight {
    [mentorType: string]: {
        [topicId: string]: number
    }
}

@Component()
export default class ConnectednessHeatmap extends Vue {
    @Prop topics = p<ITopic[]>({
        required: true
    });
    @Prop categories = p<string[]>({
        required: true
    });

    renderWeights: IRenderWeight = {};
    pConnections: IUser[] = [];

    updateConnections(newConnections: IUser[]) {
        this.pConnections = newConnections;
    }

    get connections() {
        return this.pConnections;
    };

    renderColor(category: string, topicId: number) {
        const max = 1;
        const weight = (this.renderWeights[category] && this.renderWeights[category][topicId]) || 0;
        return {
            background: `rgba(34, 85, 102, ${weight / max})`
        };
    }

    updatedCategories() {
        this.categories.forEach(category => {
            this.topics.forEach(topic => {
                if (this.renderWeights[category] === undefined) {
                    this.renderWeights[category] = {};
                }
                this.renderWeights[category][topic.id] = Math.random();
            });
        });
    }

    @Watch("categories")
    changeCategories(_oldValue: string[], _newValue: string[]) {
        this.updatedCategories();
    }

    @Lifecycle
    created() {
        Fetcher.get(UserService.getUserPeers, { count: 10 })
            .on(this.updateConnections);
        this.updatedCategories();
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getUserPeers, { count: 10 })
            .off(this.updateConnections);
    }
}
</script>
