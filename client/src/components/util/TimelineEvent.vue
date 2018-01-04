<template>
    <div class="badgeContainer">
        <div class="badgeProgress">
            <h4>{{time}}</h4>
        </div>
        <div class="badgeDescription">
            <h4>{{user}}</h4>
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
import { IEvent } from "../../interfaces/models";

@Component({
    components: {
    }
})
export default class TimelineEvent extends Vue {
    @Prop event = p<IEvent>({
        required: true
    });

    get time() {
        return this.event.dayTime.time.start.time;
    }

    get user() {
        return this.event.user;
    }
}
</script>
