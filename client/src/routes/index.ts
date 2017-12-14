import Vue from "vue";
import VueRouter from "vue-router";
import Main from "../Main.vue";

import AdminView from "../components/admin/AdminView.vue";
import ConsentView from "../components/admin/Consent.vue";
import ReportedQuestions from "../components/admin/ReportedQuestions.vue";
import ErrorPermission from "../components/error/ErrorPermission.vue";

import QuestionWrapper from "../components/questions/QuestionWrapper.vue";
import ProfileView from "../components/profile/ProfileView.vue";
import AchievementsView from "../components/profile/Achievements.vue";
import CompetenciesView from "../components/profile/Competencies.vue";
import ConnectionsView from "../components/profile/Connections.vue";
import EngagementView from "../components/profile/Engagement.vue";
import NotificationsView from "../components/profile/Notifications.vue";
import UserConsentView from "../components/profile/UserConsent.vue";
import FriendView from "../components/friends/FriendView.vue";
import QuestionBrowser from "../components/questions/QuestionBrowser.vue";
import PeerView from "../components/peers/PeerView.vue";
import LeaderBoard from "../components/leaderboard/LeaderBoard.vue";
import AuthorView from "../components/author/AuthorView.vue";
import AuthorWrapper from "../components/author/AuthorWrapper.vue";

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
        path: "/question/id/:id",
        props: true,
        component: QuestionWrapper
    }, {
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
        component: UserConsentView
    }, {
        path: "/question/answer",
        name: "answer",
        component: QuestionBrowser
    }, {
        path: "/question/create",
        name: "create",
        component: AuthorView
    }, {
        path: "/question/edit/:id",
        name: "edit",
        component: AuthorWrapper,
        props: true
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
        component: ConsentView
    }, {
        path: "/admin/reported",
        name: "reported",
        component: ReportedQuestions
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

export default router;

router.beforeEach((to, _from, next) => {
    if (to.path == "/admin" || to.path == "/profile/consent") {
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
