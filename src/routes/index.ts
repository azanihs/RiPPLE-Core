import Vue from "vue";
import VueRouter from "vue-router";
import Main from "../main";

import ProfileView from "../components/profile/ProfileView.vue";
import FriendView from "../components/friends/FriendView.vue";
import QuestionView from "../components/questions/QuestionView.vue";
import PeerView from "../components/views/PeerView.vue";

Vue.use(VueRouter);

const routes = [{
    path: "/",
    component: Main,
    children: [{
        path: "",
        name: "main",
        component: ProfileView
    }, {
        path: "/view/questions",
        name: "questions",
        component: QuestionView
    }, {
        path: "/view/friends",
        name: "friends",
        component: FriendView
    }, {
        path: "/view/peers",
        name: "peers",
        component: PeerView
    }]
}];

export default new VueRouter({
    routes
});

