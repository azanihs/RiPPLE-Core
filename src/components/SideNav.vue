<template>
    <div class="navbarContainer">
        <md-layout md-flex="100" md-hide-xsmall md-hide-small md-hide-medium>
            <div class="profileContainer">
                <div class="imageContainer">
                    <img :src="personalAvatar" />
                </div>
                <h5>Your Name</h5>
                <h4>Course Name</h4>
            </div>
        </md-layout>
        <md-layout md-hide-large-and-up>
            <md-icon>menu</md-icon>
        </md-layout>
        <ul>
            <li v-for="link in links" :key="link.href">
                <router-link :to="link.href" tag="md-button" class="routerLink">
                    <span md-hide-large-and-up>{{ link.text }}</span>
                    <md-icon>{{link.icon}}</md-icon>
                </router-link>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.navbarContainer {
    background-color: #1d323a;
    color: #f2f2f2;
}

.profileContainer {
    text-align: center;
    margin: auto;
    margin-bottom: 1em;
}

.profileContainer .imageContainer {
    width: 100px;
    height: 100px;
    padding: 10px;
    margin: auto;
}

.imageContainer img {
    width: 100%;
    height: auto;
    border-radius: 100%;
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

ul>li {
    list-style: none;
    padding: 0px;
    margin: 0px !important;
}

.routerLink {
    width: 100%;
    margin: 0px;
    display: flex;
    flex: 1;
    justify-content: space-between;
    padding: 5px 10px;
    border-radius: 0px;
    border-top: 1px solid #274550;
}

.routerLink:last-child {
    border-bottom: 1px solid #274550;
}

.routerLink>i {
    margin-left: 0px;
    margin-right: 0px;
    color: #4d656d;
}

a.routerLink,
a.routerLink:hover {
    text-decoration: none !important;
}

.router-link-exact-active.router-link-active .linkButton.md-icon-button {
    border-radius: 0px;
    margin: 0px;
}

.router-link-exact-active.router-link-active,
.router-link-exact-active.router-link-active:hover {
    /* Sets the background colour of the currently selected item */
    background-color: #ffffff !important;
    color: #111 !important;
}

h4 {
    font-size: 1em;
    margin: 0px;
    padding: 0px;
    color: #aaa;
}
</style>

<script lang="ts">
import { Vue, Component, Prop } from "av-ts";
import UserService from "../services/UserService";

@Component()
export default class SideNav extends Vue {
    personalAvatar = UserService.getLoggedInUser().self.image;

    links = [{
        text: "Profile",
        href: "/",
        icon: "widgets"
    }, {
        text: "Answer",
        href: "/view/questions",
        icon: "lightbulb_outline"
    }, {
        text: "Connect",
        href: "/view/peers",
        icon: "group"
    }, {
        text: "Leader Boards",
        href: "/view/leaderboard",
        icon: "assignment"
    }];
}
</script>
