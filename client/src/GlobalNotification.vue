<template>
    <div class="snackWrapper" :class="snackbarClass">
        <div class="snackbar">
            <span>{{ networkMessage }}</span>
            <md-button @click="closeSnackbar" class="md-accent">Close</md-button>
        </div>
    </div>
</template>

<style scoped>
    .snackWrapper {
        position: fixed;
        left: 0px;
        bottom: 0px;
        width: 100%;
        z-index: 5000;

        display: flex;
        justify-content: center;
        align-items: center;
        pointer-events: none;
        transition: bottom 250ms ease;
    }

    .snackbar {
        pointer-events: initial;

        max-width: 90%;
        background-color: #222;
        color: #f2f2f2;

        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    span {
        margin: 6px 0px 6px 24px;
        flex-grow: 0;
        text-overflow: ellipsis;
        overflow: hidden;
    }

    .snackWrapper.closed {
        bottom: -50px;
    }

</style>

<script lang="ts">
    import { Vue, Component, Lifecycle } from "av-ts";
    import { Notification } from "./interfaces/models";
    import { getBus, NEW_QUEUE_ITEM } from "./util";

    @Component
    export default class GlobalNotification extends Vue {
        pEventQueue: Notification[] = [];
        networkMessage: string | undefined = undefined;
        snackbarCloseTimeout: number | undefined = undefined;

        snackbarIsClosed = true;

        get snackbarClass() {
            return {
                "closed": this.snackbarIsClosed
            };
        }
        updateQueue(newItem: Notification) {
            // If the queue was quiet before, trigger first cycle
            if (this.pEventQueue.length === 0) {
                this.$nextTick(() => this.cycleQueue());
            }

            this.pEventQueue.push(newItem);
        }

        closeSnackbar() {
            this.snackbarIsClosed = true;

            if (this.snackbarCloseTimeout !== undefined) {
                window.clearTimeout(this.snackbarCloseTimeout);
            }

            // Wait for the snackbar to close before opening it again
            setTimeout(() => {
                this.shiftQueue();
                this.cycleQueue();
            }, 250);
        }

        showSnackbar() {
            this.snackbarIsClosed = false;
            this.snackbarCloseTimeout = window.setTimeout(() => this.closeSnackbar(), 5000);
        }

        shiftQueue() {
            this.pEventQueue.shift();
        }

        cycleQueue() {
            if (this.pEventQueue.length > 0) {
                const notification = this.pEventQueue[0];
                this.networkMessage = notification.description;
                this.showSnackbar();
            } else {
                this.snackbarIsClosed = true;
            }
        }

        @Lifecycle
        created() {
            getBus().$on(NEW_QUEUE_ITEM, this.updateQueue);
        }

        @Lifecycle
        destroyed() {
            getBus().$off(NEW_QUEUE_ITEM, this.updateQueue);
        }
    }
</script>
