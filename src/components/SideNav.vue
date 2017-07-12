<template>
    <div class="navbarContainer">
        <div class="profileContainer">
            <div class="imageContainer">
                <img :src="personalAvatar" />
            </div>
            <h5>Your Name</h5>
            <h4>Course Name</h4>
            <hr />
        </div>
        <ul>
            <li v-for="link in links"
                :key="link.href">
                <router-link :to="link.href">
                    <md-button class="linkButton">{{ link.text }}</md-button>
                </router-link>
            </li>
        </ul>
    </div>
</template>

<style scoped>
    .navbarContainer {
        position: absolute;
        height: 100%;
        width: 12.5%;
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
    
    .router-link-exact-active.router-link-active .linkButton,
    .router-link-exact-active.router-link-active .linkButton:hover {
        /* Sets the background colour of the currently selected item */
        background-color: #ffffff;
        color: #111;
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
    import PeerRepository from "../repositories/PeerRepository";

    @Component()
    export default class SideNav extends Vue {
        personalAvatar = PeerRepository.getMany(1)[0].image;

        links = [{
            text: "Profile",
            href: "/"
        }, {
            text: "View Questions",
            href: "/view/questions"
        }, {
            text: "Connect To Peers",
            href: "/view/peers"
        }];
    }
</script>
