<template>
    <md-card class="card">
        <md-layout>
            <h2>Social Connectedness</h2>
            <table v-once class="connectedTable">
                <thead>
                    <tr>
                        <th v-for="topic in topics" :key="topic">
                            {{topic}}
                        </th>
                    </tr>
                </thead>
                <tbody>
    
                </tbody>
            </table>
            <md-table v-once class="connectedContainer">
                <md-table-header>
                    <md-table-row>
                        <md-table-head class="tableHead"></md-table-head>
    
                    </md-table-row>
                </md-table-header>
                <md-table-body>
                    <md-table-row v-for="mentorType in categories" :key="mentorType">
                        <md-table-cell class="tableCell">{{mentorType}}</md-table-cell>
                        <md-table-cell class="pad" v-for="topic in topics" :key="topic" :style="renderColor(mentorType, topic)">
                            {{renderWeights[mentorType][topic] || 0}}
                        </md-table-cell>
                    </md-table-row>
                </md-table-body>
            </md-table>
        </md-layout>
    </md-card>
</template>

<style>
.connectedContainer .md-table-head-container {
    /*TODO: Move out of global scope */
    padding: 0px !important;
    display: flex;
    height: auto !important;
    border-right: 1px solid #e0e0e0;
}

.connectedContainer td:last-of-type .md-table-cell-container {
    border-right: 1px solid #e0e0e0;
}

.connectedContainer tr:last-of-type .md-table-cell-container {
    border-bottom: 1px solid #e0e0e0;
}
</style>
<style scoped>
.pad {
    margin: 1px;
}

.card {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    flex: 1;
    padding: 16px;
}

.connectedContainer {
    width: 100%;
}


h2 {
    width: 100%;
    margin-top: 0px;
}

td,
th {
    border: 1px solid #e0e0e0 !important;
    height: auto !important;
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
import { Vue, Prop, Lifecycle, Component } from "av-ts";

@Component()
export default class ConnectednessHeatmap extends Vue {
    @Prop data;
    @Prop topics;
    @Prop categories;

    renderWeights = {};

    renderColor(category, topic) {
        const max = this.data.connections.reduce((max, x) => max > x.weight ? max : x.weight, 0);
        const weight = (this.renderWeights[category] && this.renderWeights[category][topic]) || 0;
        return {
            background: `rgba(34, 85, 102, ${weight / max})`
        };
    }

    @Lifecycle
    created() {
        this.categories.forEach(category => {
            this.renderWeights[category] = this.data.connections
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
}
</script>
