<template>
  <md-layout md-flex="100"
             md-gutter="16">
      <md-layout md-flex="33"
                 md-gutter
                 v-for="(connection, i) in connections"
                 :key="i">
          <current-connection-card :user="connection">
              Request
          </current-connection-card>
      </md-layout>
  </md-layout>
</template>

<style scoped>
</style>

<script lang="ts">
import { Vue, Component, Prop, p } from "av-ts";
import { IUser } from "../../interfaces/models";

import CurrentConnectionCard from "./CurrentConnectionCard.vue";

@Component({
    components: {
        CurrentConnectionCard
    }
})
export default class CurrentConnectionSearch extends Vue {
    @Prop connections = p<IUser[]>({
        required: true
    })
}
</script>
