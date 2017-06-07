<style scoped>
    .navbarContainer {
        position: absolute;
        height: 100%;
        background-color: #1d323a;
        color: #f2f2f2;
    }

    .profileContainer hr {
        width: 75%;
        border: none;
        border-bottom: 1px solid #274550;
        margin: 1em auto;
    }

    .profileContainer {
        text-align: center;
    }

    .profileContainer .imageContainer {
        width: 100px;
        height: auto;
        padding: 10px;
        margin: auto;
    }
    .imageContainer img {
        width: 100%;
        height: auto;
        border-radius: 100%;
        box-shadow: 2px 2px 2px #999;
    }

    .profileContainer h5 {
        font-weight: normal;
        font-size: 1em;
        margin: 0px auto;
    }

    ul {
        margin: 0px;
        padding: 0px;
        padding: 0px;
    }

    ul > li {
        list-style: none;
        padding: 0px;
        margin: 0px;

    }

    .linkButton {
        width: 100%;
        box-sizing: border-box;
        margin: 0px;
        color: #f2f2f2;
        text-align: left;
        border-radius: 0px;
    }

    /* Sets the background colour of the currently selected item */
    .router-link-exact-active.router-link-active .linkButton {
        background-color: #ffffff;
        color: #111;
    }

</style>

<template>
    <div class="navbarContainer">
        <div class="profileContainer">
            <div class="imageContainer">
                <img src="https://placebear.com/200/200" />
            </div>
            <h5>Nicholas Achilles</h5>
            <hr />
        </div>
        <ul>
            <li v-for="link in links">
                <router-link :to="link.href"><md-button class="linkButton">{{ link.text }}</md-button></router-link>
            </li>
        </ul>
    </div>
</template>

<script lang="ts">
    import { Vue, Component, Prop } from "av-ts";

    @Component
    export default class SideNav extends Vue {
        links = [{
            text: "Profile",
            href: "/"
        }, {
            text: "Visulisations",
            href: "#"
        }, {
            text: "View Questions",
            href: "/view/questions"
        }, {
            text: "Find Friends",
            href: "/view/friends"
        }];
    }
</script>
