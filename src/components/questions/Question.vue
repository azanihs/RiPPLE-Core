<template>
    <div>
        <scatter ref="scatter"
                 :propData="competencies"></scatter>
    </div>
</template>

<style scoped>
    div {
        width: 25%;
        height: 300px;
    }
</style>


<script lang="ts">
    import { Vue, Component, Lifecycle, Prop } from "av-ts";
    import ScatterChart1D from "../charts/ScatterChart1D.vue";
    import UserService from "../../services/UserService";

    @Component({
        components: {
            "scatter": ScatterChart1D
        }
    })
    export default class Question extends Vue {

        get competencies() {
            return UserService.userCompetencies().data.datasets[1].data.map(x => ({
                value: x,
                fill: "#8bc34a"
            }));
        }

        @Lifecycle
        mounted() {
            setTimeout(() => {
                (this.$refs["scatter"] as ScatterChart1D).updateDimensions();
                (this.$refs["scatter"] as ScatterChart1D).redraw();
            }, 250);
        }
    }
</script>
