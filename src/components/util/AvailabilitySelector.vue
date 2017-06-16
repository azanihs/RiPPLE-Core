<template>
    <md-layout>
        <h2>
            We would like to know when you are available so that we can match you up with people who have similar schedules
        </h2>
        <md-table v-once class="table">
            <md-table-header>
                <md-table-row>
                    <md-table-head>Activity</md-table-head>
                    <md-table-head v-for="time in preferenceTimes" :key="time">{{ time == 12 ? `${time}pm` : (time < 12 ? `${time}am` : `${time-12}pm`) }}</md-table-head>
                </md-table-row>
            </md-table-header>

            <md-table-body>
                <md-table-row v-for="activity in preferenceActivities" :key="activity">
                    <md-table-cell class="alignLeft">
                        {{ activity }}
                    </md-table-cell>
                    <md-table-cell v-for="time in preferenceTimes" :key="time">
                        <md-checkbox :id="`${activity}_${time}`" :name="`${activity}_${time}`"></md-checkbox>
                    </md-table-cell>
                </md-table-row>
            </md-table-body>
        </md-table>
    </md-layout>
</template>

<style scoped>
    h2 {
        color: #999;
        font-size: 1em;
        margin: 0px;
        padding: 0px;
    }

    .md-checkbox {
        margin: 0px auto;
    }

    .table {
        border: 1px solid #ccc;
        width: 100%;
    }
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle, Prop } from "av-ts";
    import { Question } from "../../interfaces/models";

    @Component()
    export default class AvailabilitySelector extends Vue {
        preferenceActivities: string[] = ["Be A Mentor", "Need a mentor", "Study with peer"];
        preferenceTimes: number[] = new Array(13).fill(0).map((x, i) => i + 8);


        addNewRow() {

        }

        deleteRow() {

        }

    }
</script>
