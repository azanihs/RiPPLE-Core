<style scoped>
    ul > li:first-of-type {
        cursor: pointer;
    }
</style>

<template>
    <ul>
        <li @click="toggleMenu">{{ showLinks ? "Hide Menu" : "Show Menu" }}
        <li v-if="showLinks" v-for="link in links">
            <router-link :to="link.href">{{ link.text }}</router-link>
        </li>
    </ul>
</template>
<script lang="ts">
    import { Vue, Component, Prop } from "av-ts";

    @Component
    export default class SideNav extends Vue {
        links = [{
            text: "Home",
            href: "/"
        }, {
            text: "View Questions",
            href: "/view/questions"
        }, {
            text: "View Friends",
            href: "/view/friends"
        }];

        showLinks: boolean = false;
        toggleMenu() {
            this.showLinks = !this.showLinks;
        }
    }
</script>
