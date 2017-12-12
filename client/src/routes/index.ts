import Vue from "vue";
import VueRouter from "vue-router";
import Main from "../Main.vue";

import AdminView from "../components/admin/AdminView.vue";
import ConsentEditor from "../components/admin/ConsentEditor.vue";

import ErrorPermission from "../components/error/ErrorPermission.vue";

import ProfileView from "../components/profile/ProfileView.vue";
import AchievementsView from "../components/profile/Achievements.vue";
import CompetenciesView from "../components/profile/Competencies.vue";
import ConnectionsView from "../components/profile/Connections.vue";
import EngagementView from "../components/profile/Engagement.vue";
import NotificationsView from "../components/profile/Notifications.vue";
import ConsentFormWrapper from "../components/profile/ConsentFormWrapper.vue";
import FriendView from "../components/friends/FriendView.vue";
import QuestionBrowser from "../components/questions/QuestionBrowser.vue";
import PeerView from "../components/peers/PeerView.vue";
import LeaderBoard from "../components/leaderboard/LeaderBoard.vue";
import AuthorView from "../components/author/AuthorView.vue";

import WIP from "../components/WIP.vue";
import UserRepository from "../repositories/UserRepository";

Vue.use(VueRouter);

const routes = [{
    path: "/",
    component: Main,
    props: (x: any) => ({
        path: x.name,
        token: x.query.token,
        initCourseCode: x.query.course_code
    }),
    children: [{
        path: "/",
        name: "profile",
        component: ProfileView
    }, {
        path: "/profile/engagement",
        name: "engagement",
        component: EngagementView
    }, {
        path: "/profile/competencies",
        name: "competencies",
        component: CompetenciesView
    }, {
        path: "/profile/connections",
        name: "connections",
        component: ConnectionsView
    }, {
        path: "/profile/achievements",
        name: "achievements",
        component: AchievementsView
    }, {
        path: "/profile/notifications",
        name: "notifications",
        component: NotificationsView
    }, {
        path: "/profile/consent",
        name: "userConsent",
        component: ConsentFormWrapper
    }, {
        path: "/question/answer",
        name: "answer",
        component: QuestionBrowser
    }, {
        path: "/question/create",
        name: "create",
        component: AuthorView
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
        path: "/admin/consent",
        name: "consent",
        component: ConsentEditor
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

const router = new VueRouter({
    routes
});

router.beforeEach((_to, _from, next) => {
    if (_to.path == "/admin/consent" || _to.path == "/profile/consent") {
        next();
    } else {
        UserRepository.userHasConsentedForCourse()
            .then(hasConsented => {
                if (!hasConsented) {
                    return next("/profile/consent");
                }
                next();
            });
    }
});

export default router;
