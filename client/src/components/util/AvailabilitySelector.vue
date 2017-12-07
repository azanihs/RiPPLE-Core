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
                        <th v-for="time in times"
                            :key="time.id">{{twentyFourHourToTwelveHourPeriod(time.start.hour)}}
                        </th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="day in days"
                        :key="day.id">
                        <td>{{day.day}}</td>
                        <td v-for="time in times"
                            :key="time.id"
                            class="centerAlign"
                            :style="getCellShade(day.id, time.id)">
                            <md-checkbox :value="checkbox(day.id, time.id)"
                                         class="centerCheckbox"
                                         @change="checkboxChange(day.id, time.id)"
                                         :id="`${day.id}_${time.id}`"
                                         :name="`${day.id}_${time.id}`"></md-checkbox>
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
import { Vue, Component, Prop, p } from "av-ts";
import { IAvailability, IDay, IDayTime, ITime } from "../../interfaces/models";

@Component()
export default class AvailabilitySelector extends Vue {
    @Prop days = p<IDay[]>({
        default: () => {
            return [];
        }
    });

    @Prop times = p<ITime[]>({
        default: () => {
            return [];
        }
    })

    @Prop courseDistribution = p<number[][]>({
        default: () => {
            return [];
        }
    });

    @Prop userDistribution = p<IAvailability[]>({
        default: () => {
            return [];
        }
    });

    @Prop maxAvailable = p<number>({
        default: () => {
            return 0;
        }
    });

    pShowAvailability = true;

    get showAvailability() {
        return this.pShowAvailability;
    }
    set showAvailability(newVal) {
        this.pShowAvailability = newVal;
    }

    checkbox(localDay: number, localTime: number) {
        const { day, time } = this.localToUTC(localDay, localTime);
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

    checkboxChange(localDay: number, localTime: number) {
        const { day, time } = this.localToUTC(localDay, localTime);
        this.$emit("change", day, time);
    }

    addNewRow() {
        throw new Error("addNewRow not implemented");
    }

    deleteRow() {
        throw new Error("deleteRow not implemented");
    }

    getCellShade(localDay: number, localTime: number) {
        if (this.showAvailability) {
            let weight = 0;
            if (this.maxAvailable > 0) {
                const { day, time } = this.localToUTC(localDay, localTime);
                const courseDistributionDay = this.courseDistribution[day - 1];
                const entry = courseDistributionDay[time - 1];
                weight = entry / this.maxAvailable;
            }
            // Perferably have a lookup table generated on mount
            return {
                background: `rgba(34, 85, 102, ${weight})`
            };
        }
    }

    convertDay(day?: number): number {
        if (day === undefined || this.days.length == 0) {
            throw new Error("Missing day");
        }
        if (day < 1) {
            return day + 7;
        } else if (day > 7) {
            return day - 7;
        } else {
            return day;
        }
    }

    convertTime(time?: number): number {
        if (time === undefined) {
            throw new Error("Missing day time");
        }

        if (time < 1) {
            return time + 24;
        } else if (time > 24) {
            return time - 24;
        } else {
            return time;
        }
    }

    localToUTC(localDay?: number, localTime?: number): IDayTime {
        if (localDay === undefined || localTime === undefined) {
            throw new Error("Missing localday or localtime");
        }

        const offset = new Date().getTimezoneOffset() / 60;
        let time = localTime + offset;
        let day = localDay;
        if (time < 1) {
            day--;
        } else if (time >= 24) {
            day++;
        }

        const dayTime: IDayTime = {
            day: this.convertDay(day),
            time: this.convertTime(time)
        };
        return dayTime;
    }
}
</script>
