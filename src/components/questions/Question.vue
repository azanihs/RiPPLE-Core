<template>
    <div>
        <chart type="bar"
               :data="competencies"></chart>
        {{$route.params.id}}
    </div>
</template>

<style scoped>
    div {
        width: 25%;
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
    export default class Question extends Vue {

        get competencies() {
            return UserService.userCompetencies().data;
        }
    }
</script>
