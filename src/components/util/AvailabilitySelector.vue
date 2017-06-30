<template>
    <md-layout>
        <h2>
            <md-icon>access_time </md-icon> Select your weekly availability so that we can match you up with people who have similar schedules
        </h2>
        <md-table v-once
                  class="table">
            <md-table-header>
                <md-table-row>
                    <md-table-head>Day</md-table-head>
                    <md-table-head v-for="time in preferenceTimes"
                                   :key="time">{{ twentyFourHourToTwelveHourPeriod(time) }}
                    </md-table-head>
                </md-table-row>
            </md-table-header>
    
            <md-table-body>
                <md-table-row v-for="activity in preferenceActivities"
                              :key="activity">
                    <md-table-cell class="alignLeft">
                        {{ activity }}
                    </md-table-cell>
                    <md-table-cell v-for="time in preferenceTimes"
                                   :key="time">
                        <md-checkbox @change="checkboxChange"
                                     :id="`${activity}_${time}`"
                                     :name="`${activity}_${time}`"></md-checkbox>
                    </md-table-cell>
                </md-table-row>
            </md-table-body>
        </md-table>
    </md-layout>
</template>

<style scoped>
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
        preferenceActivities: string[] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
        preferenceTimes: number[] = new Array(13).fill(0).map((x, i) => i + 8);

        /**
        *   Converts a twenty four hour time to twelve hour with an "am" or "pm" suffix
        *   @param {number} time Twenty four hour time to convert to twelve hour
        *   @return {string} Twelve hour representation of time with "am" or "pm" suffix
        */
        twentyFourHourToTwelveHourPeriod(twentyHourTime: number): string {
            const time = +twentyHourTime;
            if (time == 12) {
                return `${time}pm`;
            } else if (time < 12) {
                return `${time}am`;
            }
            return `${time - 12}pm`;
        }

        checkboxChange() {
            this.$emit("change");
        }

        addNewRow() {
            throw new Error("addNewRow not implemented");
        }

        deleteRow() {
            throw new Error("deleteRow not implemented");
        }

    }
</script>
