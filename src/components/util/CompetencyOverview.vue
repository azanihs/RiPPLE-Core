<template>
    <md-layout md-gutter="16">
        <h2>Competency Overview</h2>
        <md-layout md-flex="50">
            <chart :type="'bar'"
                   :data="competencies.data"
                   :options="competencies.options"></chart>
        </md-layout>
    </md-layout>
</template>
<style scoped>
    h2 {
        width: 100%;
        padding-top: 0.75em;
    }
</style>

<script lang="ts">
    import { Vue, Component, Prop } from "av-ts";
    import Chart from "../charts/Chart.vue";
    import UserService from "../../services/UserService";

    @Component({
        components: {
            "chart": Chart
        }
    })
    export default class CompetencyOverview extends Vue {

        get competencies() {
            return UserService.userCompetencies();
        }
    }
</script>
