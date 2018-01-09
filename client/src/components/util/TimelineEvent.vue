<template>
    <div class="badgeContainer">
        <div class="badgeProgress">
            <h4>{{time}}</h4>
        </div>
        <div class="badgeDescription">
            <h4>{{user.name}}</h4>
            <md-avatar>
                <img :src="user.image"
                     :alt="user.name">
            </md-avatar>
            <p>Location</p>
        </div>
    </div>
</template>

<style scoped>
.badgeContainer {
    display: flex;
    width: 100%;
    align-items: center;
    background-color: #fafafa;
    margin-bottom: 16px;
}

.badgeDescription {
    padding-left: 8px;
}

.badgeProgress {
    position: relative;
    height: 100%;
    background-color: #eee;
    align-items: center;
    display: flex;
    padding: 0px 1.25em;
    border-right: 1px solid #e1e1e1;
}

</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { ILocalisedEvent } from "../../interfaces/models";

@Component({
    components: {
    }
})
export default class TimelineEvent extends Vue {
    @Prop event = p<ILocalisedEvent>({
        required: true
    });

    formatAMPM(date: Date): string {
        // From: https://stackoverflow.com/questions/8888491/how-do-you-display-javascript-datetime-in-12-hour-am-pm-format
        let hours = date.getHours();
        let minutes = date.getMinutes();
        const ampm = hours >= 12 ? "pm" : "am";
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        const displayMins = minutes < 10 ? "0" + minutes : minutes.toString();
        const strTime = hours + ":" + displayMins + " " + ampm;
        return strTime;
    }


    get time() {
        if (this.event) {
            return this.formatAMPM(new Date(this.event.date));
        } else {
            return "";
        }
    }

    get user() {
        if (this.event) {
            return this.event.user;
        } else {
            return "";
        }
    }
}
</script>
