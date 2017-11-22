import Vue from "vue";
import VueRouter from "vue-router";
import Main from "../Main.vue";

import AdminView from "../components/admin/AdminView.vue";
import ErrorPermission from "../components/error/ErrorPermission.vue";

import ProfileView from "../components/profile/ProfileView.vue";
import FriendView from "../components/friends/FriendView.vue";
import QuestionBrowser from "../components/questions/QuestionBrowser.vue";
import PeerView from "../components/peers/PeerView.vue";
import LeaderBoard from "../components/leaderboard/LeaderBoard.vue";
import AuthorView from "../components/author/AuthorView.vue";

import WIP from "../components/WIP.vue";

Vue.use(VueRouter);

const routes = [{
    path: "/",
    component: Main,
    props: x => ({
        path: x.name,
        token: x.query.token,
        initCourseCode: x.query.course_code
    }),
    children: [{
        path: "/",
        name: "profile",
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
        path: "/view/author",
        name: "author",
        component: AuthorView
    }, {
        path: "/admin",
        name: "admin",
        component: AdminView
    }, {
        path: "/error/403",
        name: "errorPermission",
        component: ErrorPermission
    }, {
        path: "*",
        name: "error",
        component: WIP
    }]
}];

export default new VueRouter({
    routes
});

