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
import { Vue, Prop, Lifecycle, Component, Watch } from "av-ts";

@Component()
export default class ConnectednessHeatmap extends Vue {
    @Prop connections;
    @Prop topics;
    @Prop categories;

    renderWeights = {};

    renderColor(category, topic) {
        const max = this.connections.reduce((max, x) => max > x.weight ? max : x.weight, 0);
        const weight = (this.renderWeights[category] && this.renderWeights[category][topic]) || 0;
        return {
            background: `rgba(34, 85, 102, ${weight / max})`
        };
    }

    updatedCategories() {
        this.categories.forEach(category => {
            this.renderWeights[category] = this.connections
                .filter(x => x.type == category)
                .reduce((categoryWeight, connection) => {
                    if (categoryWeight[connection.topic] === undefined) {
                        categoryWeight[connection.topic] = connection.weight;
                    } else {
                        categoryWeight[connection.topic] += connection.weight;
                    }
                    return categoryWeight;
                }, {});
        });
    }

    @Watch("categories")
    changeCategories() {
        this.updatedCategories();
    }

    @Lifecycle
    created() {
        this.updatedCategories();
    }
}
</script>
