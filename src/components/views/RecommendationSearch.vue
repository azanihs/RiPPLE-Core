<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100">
            <!-- Plot topics -->
            <chart type="bar"></chart>
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
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import RecommendationCard from "./RecommendationCard.vue";

@Component({
    components: {
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

    searchType = "";
    @Lifecycle
    created() {
        this.searchType = this.searchTypes[0];
    }

}
</script>
