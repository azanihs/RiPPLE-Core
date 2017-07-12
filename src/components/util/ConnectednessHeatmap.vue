<template>
    <md-layout>
        <h2>Social Connectedness</h2>
        <md-table v-once
                  class="connectedContainer">
            <md-table-header>
                <md-table-row>
                    <md-table-head class="tableHead"></md-table-head>
                    <md-table-head v-for="topic in topics"
                                   :key="topic">
                        {{topic}}
                    </md-table-head>
                </md-table-row>
            </md-table-header>
            <md-table-body>
                <md-table-row v-for="mentorType in categories"
                              :key="mentorType">
                    <md-table-cell class="tableCell">{{mentorType}}</md-table-cell>
                    <md-table-cell v-for="topic in topics"
                                   :key="topic"
                                   :style="renderColor(mentorType, topic)">
                        {{renderWeights[mentorType][topic] || 0}}
                    </md-table-cell>
                </md-table-row>
            </md-table-body>
        </md-table>
    </md-layout>
</template>

<style>
    .connectedContainer .md-table-head-container {
        /*TODO: Move out of global scope */
        padding: 0px !important;
        display: flex;
        height: auto !important;
    }
</style>
<style scoped>
    .connectedContainer {
        width: 100%;
    }
    
    h2 {
        width: 100%;
        padding-top: 0.75em;
    }
    
    td,
    th {
        border: 1px solid #eee !important;
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
