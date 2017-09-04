<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100"
                   class="componentSeparator">
            <table class="table">
                <thead>
                    <tr>
                        <th>Topics</th>
                        <th v-for="sType in searchTypes"
                            :key="sType">{{ sType }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="topic in topics"
                        :key="topic.id">
                        <td>
                            <span>{{ topic.name }}</span>
                            <div class="cellOverlay"
                                 :style="getCellWeight(topic)"></div>
                        </td>
                        <td v-for="sType in searchTypes"
                            :key="sType"
                            class="centerAlign">
                            <md-checkbox class="centerCheckbox"
                                         :disabled="checkboxIsDisabled(sType, topic)"
                                         @change="checkboxChange"
                                         :id="`${sType}_${topic}`"
                                         :name="`${sType}_${topic}`"></md-checkbox>
                        </td>
                    </tr>
                </tbody>
            </table>
        </md-layout>
        <md-tabs md-fixed
                 class="md-transparent">
            <md-tab md-label="Find"
                    class="tab">
                <md-layout md-flex="100"
                           md-gutter="16">
                    <md-layout md-flex="33"
                               md-gutter
                               v-for="(recommendation, i) in recommendations"
                               :key="i">
                        <recommendation-card :user="recommendation">
                            Request
                        </recommendation-card>
                    </md-layout>
                </md-layout>
            </md-tab>
            <md-tab md-label="Review"
                    class="tab">
                <md-layout md-flex="100"
                           md-gutter="16">
                    <md-layout md-flex="33"
                               md-gutter
                               v-for="(recommendation, i) in requests"
                               :key="i">
                        <recommendation-card :user="recommendation">
                            Request
                        </recommendation-card>
                    </md-layout>
                </md-layout>
            </md-tab>
        </md-tabs>
    </md-layout>
</template>

<style scoped>
.tab {
    padding-left: 2px !important;
    padding-right: 2px !important;
}

.table {
    border: none;
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

.table tbody td:first-child {
    position: relative;
}

.table thead tr {
    background-color: #256;
    color: #f2f2f2;
}

.table tbody tr:nth-child(even) {
    background-color: #efefef;
}

.table tr td,
.table thead tr th {
    text-align: center;
    padding: 8px 0px;
}

.cellOverlay {
    position: absolute;
    left: 0px;
    top: 5%;
    width: 0px;
    height: 90%;
    border: 1px solid transparent;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";

import { Topic } from "../../interfaces/models";

import UserService from "../../services/UserService";

import RecommendationCard from "./RecommendationCard.vue";

import PropUpdate from "../mixins/PropUpdate";

@Component({
    components: {
        RecommendationCard
    }
})
export default class RecommendationSearch extends Vue {
    @Prop
    searchTypes = p<string[]>({
        required: true,
        type: Array
    });

    @Prop
    topics = p<Topic[]>({
        required: true,
        type: Array
    });


    competencies = [];

    pRecommendations = [];
    pRequests = [];

    @Lifecycle
    created() {
        //UserService.subscribe("getRecommenedConnections", this.PropUpdate("pRecommendations"));
        //UserService.unsubscribe("getOutstandingRequests", this.PropUpdate("pRequests"));

        /*this.competencies = UserService.userCompetencies(this.topics)
            .ownScores
            .filter(x => x.source == x.target)
            .map(x => x.competency);*/
    }

    get recommendations() {
        return this.pRecommendations;
    }

    get requests() {
        return this.pRequests;
    }

    checkboxChange() {

    }

    checkboxIsDisabled(sType, topic) {
        if (sType == "Provide Mentorship") {
            const weight = this.competencies[this.topics.findIndex(x => x == topic)];
            return weight <= 85;
        }

        return false;
    }

    getColour(c) {
        if (c < 50) {
            return "rgba(255, 99, 132, ";
        } else if (c >= 50 && c < 85) {
            return "rgba(255, 206, 86, ";
        } else if (c >= 85) {
            return "rgba(34, 85, 102, ";
        }
    };

    getCellWeight(topic) {
        const weight = this.competencies[this.topics.findIndex(x => x == topic)];
        return {
            background: `${this.getColour(weight)}${0.4})`,
            borderColor: `${this.getColour(weight)}1)`,
            width: `${weight}%`
        };
    }
}
</script>
