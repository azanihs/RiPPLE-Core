<template>
    <md-card md-with-hover
             class="recommendationsCard">
        <md-card-header class="fullWidth">
            <md-avatar>
                <md-avatar>
                    <img :src="user.image"
                         :alt="user.name">
                </md-avatar>
            </md-avatar>
            <div class="md-title">{{user.name}}</div>
            <div class="md-subhead">
                <topic-chip v-for="prof in user.proficiencies"
                            :key="prof"
                            linkTo="/view/peers">
                    {{prof}}
                </topic-chip>
            </div>
        </md-card-header>
        <md-card-actions>
            <md-button>End Connection</md-button>
        </md-card-actions>
    </md-card>
</template>

<style scoped>
.autoComplete {
    margin-bottom: 0px;
}

.fullWidth {
    width: 100%;
}

.flex {
    display: flex;
    flex: 1;
    min-width: 100%;
    padding-bottom: 0px;
}

</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { IUser } from "../../interfaces/models";

import TopicChip from "../util/TopicChip.vue";

@Component({
    components: {
        TopicChip
    }
})
export default class CurrentConnectionCard extends Vue {
    @Prop user = p<IUser>({
        required: true
    });
}
</script>
