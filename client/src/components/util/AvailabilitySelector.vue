<template>
    <md-layout>
        <md-card>
            <div class="spaceBetween">
                <h2>
                    Select your availability to match with people who have similar schedules
                </h2>
                <md-switch v-model="showAvailability"
                           class="md-primary switch"
                           id="availabilitySwitch"
                           name="availabilitySwitch">Show Student Availability</md-switch>
            </div>
            <table class="table">
                <thead>
                    <tr>
                        <th>Day</th>
                        <th v-for="time in pAvailableTimes"
                            :key="time">{{ twentyFourHourToTwelveHourPeriod(time) }}
                        </th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="activity in pAvailableDays"
                        :key="activity">
                        <td>{{ preferenceActivities[activity] }}</td>
                        <td v-for="time in pAvailableTimes"
                            :key="time"
                            class="centerAlign"
                            :style="getCellShade(activity, time)">
                            <md-checkbox class="centerCheckbox"
                                         @change="checkboxChange"
                                         :id="`${activity}_${time}`"
                                         :name="`${activity}_${time}`"></md-checkbox>
                        </td>
                    </tr>
                </tbody>
            </table>
        </md-card>
    </md-layout>
</template>

<style scoped>
.spaceBetween {
    display: flex;
    flex: 1;
    justify-content: space-between;
}

h2 {}

.switch {}

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
import { Vue, Component, Watch, Lifecycle, Prop, p } from "av-ts";
import { Question } from "../../interfaces/models";

@Component()
export default class AvailabilitySelector extends Vue {
    preferenceActivities: string[] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    preferenceTimes: number[] = new Array(13).fill(0).map((x, i) => i + 8);

    pShowAvailability = true;

    pAvailableDays: number[] = [1, 2, 3, 4, 5];
    pAvailableTimes: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];

    pMaxAvailable: number = 0;

    @Prop course = p({
        type: Array,
        default: () => {
            return [];
        }
    });

    get showAvailability() {
        return this.pShowAvailability;
    }
    set showAvailability(newVal) {
        this.pShowAvailability = newVal;
    }

    /**
    *   Converts a twenty four hour time to twelve hour with an "am" or "pm" suffix
    *   @param {number} time Twenty four hour time to convert to twelve hour
    *   @return {string} Twelve hour representation of time with "am" or "pm" suffix
    */
    twentyFourHourToTwelveHourPeriod(twentyHourTime: number): string {
        const time = 7 + twentyHourTime;
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

    getCellShade(day, time) {
        if (this.showAvailability) {
            let weight = 0;
            if (this.pMaxAvailable > 0) {
                for (let i = 0; i < this.course.length; i++) {
                    if (this.course[i].day == day && this.course[i].time == time) {
                        weight = this.course[i].entries / this.pMaxAvailable;
                        break;
                    }
                }
            }
            // Perferably have a lookup table generated on mount
            return {
                background: `rgba(34, 85, 102, ${weight})`
            };
        }
    }

    @Watch("course")
    handleAvailabilityChange() {
        for (let i = 0; i < this.course.length; i++) {
            if (this.course[i].entries > this.pMaxAvailable) {
                this.pMaxAvailable = this.course[i].entries;
            }
        }
    }
}
</script>
