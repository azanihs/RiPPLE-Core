<template>
            <md-snackbar md-position="bottom center"
            ref="snackbar"
            md-duration="4000">
            <span>{{networkMessage}}</span>
            <md-button class="md-accent"
                @click="$refs.snackbar.close()">Close</md-button>
        </md-snackbar>
</template>

<style scoped>
</style>

<script lang="ts">
    import { Vue, Component, Lifecycle } from "av-ts";


    @Component
    export default class GlobalNotification extends Vue {

    }
</script>
