<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100"
                   class="componentSeparator">
            <!-- Plot topics -->
            <recommendation-filter :topics="topics"
                                   :types="searchTypes">
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
                            :key="topic">
                            <td>
                                {{ topic }}
                            </td>
                            <td v-for="sType in searchTypes"
                                :key="sType"
                                class="centerAlign"
                                :style="getCellShade(topic)">
                                <md-checkbox class="centerCheckbox"
                                             @change="checkboxChange"
                                             :id="`${sType}_${topic}`"
                                             :name="`${sType}_${topic}`"></md-checkbox>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </recommendation-filter>
        </md-layout>
        <md-tabs md-fixed
                 class="md-transparent">
            <md-tab md-label="Find"
                    class="tab">
                <md-layout md-flex="100"
                           md-gutter="16">
                    <md-layout md-flex="33"
                               md-gutter
                               v-for="(recommendation, i) in generator(searchType).recommendations"
                               :key="i">
                        <recommendation-card :data="recommendation">
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
                               v-for="(recommendation, i) in generator(searchType).requests"
                               :key="i">
                        <recommendation-card :data="recommendation">
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
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import RecommendationCard from "./RecommendationCard.vue";
import RecommendationFilter from "./RecommendationFilter.vue";

@Component({
    components: {
        RecommendationFilter,
        RecommendationCard
    }
})
export default class RecommendationSearch extends Vue {
    @Prop
    searchTypes = p({
        required: true,
        type: Array
    }) as string[];

    @Prop
    generator = p({ // Function takes in arguments from searchTypes
        required: true,
        type: Function
    }) as Function;

    @Prop
    topics = p({
        required: true,
        type: Array
    }) as string[];

    searchType = "";

    @Lifecycle
    created() {
        this.searchType = this.searchTypes[0];
    }

    checkboxChange() {

    }

    getCellShade(time) {
        const weight = Math.random() < 0.75 ? 0 : Math.random() - 0.25;
        // Perferably have a lookup table generated on mount
        return {
            background: `rgba(34, 85, 102, ${weight})`
        };
    }
}
</script>
