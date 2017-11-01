<template>
    <md-layout md-flex="100" class="marginTop">
        <md-card>
            <div class="errorContainer">
                <h3>You do not have permission to view that page.</h3>
                <router-link class="md-button" to="/">
                    <md-icon>keyboard_return</md-icon> Home
                </router-link>
            </div>
        </md-card>
    </md-layout>
</template>

<style scoped>
.marginTop {
    margin-top: 1em;
}
.errorContainer {
    flex-direction: column;
    justify-content: flex-start;
}
</style>


<script lang="ts">
import { Vue, Component } from "av-ts";

@Component()
export default class ErrorPermission extends Vue {

}
</script>
