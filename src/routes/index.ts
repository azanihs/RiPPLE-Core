import Vue from "vue";
import VueRouter from "vue-router";
import Main from "../main";

import ProfileView from "../components/profile/ProfileView.vue";
import FriendView from "../components/friends/FriendView.vue";
import QuestionBrowser from "../components/questions/QuestionBrowser.vue";
import PeerView from "../components/peers/PeerView.vue";
import LeaderBoard from "../components/leaderboard/LeaderBoard.vue";

import WIP from "../components/WIP.vue";

Vue.use(VueRouter);

const routes = [{
    path: "/",
    component: Main,
    props: x => ({
        path: x.path
    }),
    children: [{
        path: "/",
        name: "main",
        component: ProfileView
    }, {
        path: "/view/questions",
        name: "questions",
        component: QuestionBrowser
    }, {
        path: "/view/friends",
        name: "friends",
        component: FriendView
    }, {
        path: "/view/peers",
        name: "peers",
        component: PeerView
    }, {
        path: "/view/leaderboard",
        name: "leaderboard",
        component: LeaderBoard
    }, {
        path: "*",
        name: "error",
        component: WIP
    }]
}];

export default new VueRouter({
    routes
});

