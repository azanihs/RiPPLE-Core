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
                        <th v-for="time in pTimes"
                            :key="time.time">{{ twentyFourHourToTwelveHourPeriod(time.time) }}
                        </th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="activity in pAvailableDays"
                        :key="activity">
                        <td>{{ preferenceActivities[activity - 1] }}</td>
                        <td v-for="time in pTimes"
                            :key="time.time"
                            class="centerAlign"
                            :style="getCellShade(activity, time.time)">
                            <md-checkbox :value="checkbox(activity, time.time)"
                                         class="centerCheckbox"
                                         @change="checkboxChange(activity, time.time)"
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
import { Availability, CourseAvailability, Time } from "../../interfaces/models";
import Fetcher from "../../services/Fetcher";
import AvailabilityService from "../../services/AvailabilityService";

@Component()
export default class AvailabilitySelector extends Vue {
    preferenceActivities: string[] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    preferenceTimes: number[] = new Array(13).fill(0).map((x, i) => i + 8);

    pShowAvailability = true;

    pAvailableDays: number[] = [1, 2, 3, 4, 5];

    pMaxAvailable: number = 0;
    pTimes: Time[] = [];

    @Prop courseDistribution = p<CourseAvailability[]>({
        default: () => {
            return [];
        }
    });

    @Prop userDistribution = p<Availability[]>({
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

    checkbox(day, time) {
        for (let i = 0; i < this.userDistribution.length; i++) {
            const entry = this.userDistribution[i];
            if (entry.day.id == day && entry.time.id == time) {
                return true;
            }
        }
        return false;
    }

    /**
    *   Converts a twenty four hour time to twelve hour with an "am" or "pm" suffix
    *   @param {number} time Twenty four hour time to convert to twelve hour
    *   @return {string} Twelve hour representation of time with "am" or "pm" suffix
    */
    twentyFourHourToTwelveHourPeriod(time: number): string {
        if (time == 12) {
            return `${time}pm`;
        } else if (time < 12) {
            return `${time}am`;
        }
        return `${time - 12}pm`;
    }

    checkboxChange(day, time) {
        const utcTime = this.localToUTC(time);
        this.$emit("change", day, utcTime);
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
                for (let i = 0; i < this.courseDistribution.length; i++) {
                    if (this.courseDistribution[i].day == day && this.courseDistribution[i].time == time) {
                        weight = this.courseDistribution[i].entries / this.pMaxAvailable;
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

    localToUTC(local?: number): number {
        if (local === undefined) return undefined;

        const offset = new Date().getTimezoneOffset() / 60;
        return (local + offset) % 24;
    }

    serverToLocal(utcTimestamp?: number): number {
        if (utcTimestamp === undefined) return undefined;

        const offset = new Date().getTimezoneOffset() / 60;
        return (utcTimestamp - offset) % 24;
    }

    updateTimes(times: Time[]) {
        const displayTimes = times.filter(time => {
            const localTime = this.serverToLocal(time.start.hour);
            return localTime >= 8 && localTime <= 20;
        });

        let timeSlots = [];
        displayTimes.map(time => {
            timeSlots.push( {
                id: time.id, time: this.serverToLocal(time.start.hour)
            });
        });

        this.pTimes = timeSlots.sort(function(a, b) {
            return a.time - b.time;
        });
    };

    @Lifecycle
    created() {
        Fetcher.get(AvailabilityService.getUTCTimeSlots)
            .on(this.updateTimes);
    }

    @Watch("courseDistribution")
    handleCourseChange() {
        for (let i = 0; i < this.courseDistribution.length; i++) {
            if (this.courseDistribution[i].entries > this.pMaxAvailable) {
                this.pMaxAvailable = this.courseDistribution[i].entries;
            }
        }
    }
}
</script>
