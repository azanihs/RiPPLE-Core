<template>
    <md-card md-with-hover
             class="recommendationsCard">
        <md-card-header class="fullWidth">
            <div class="md-title">"John Smith"</div>
        </md-card-header>
        <md-card-content class="fullWidth flex">
            <md-input-container class="autoComplete">
                <label>Something</label>
            </md-input-container>
        </md-card-content>
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

@Component({
    components: {

    }
})
export default class CurrentConnectionCard extends Vue {
    @Prop user = p<IUser>({
        required: true
    });
}
</script>
