import Vue from "vue";
import VueRouter from "vue-router";
import Main from "../main";

import DefaultView from "components/views/DefaultView";
import FriendView from "components/views/FriendView";
import QuestionView from "components/views/QuestionView";


Vue.use(VueRouter);

const routes = [{
	path: "/",
	component: Main,
	children: [{
		path: "",
		name: "main",
		component: DefaultView
	}, {
		path: "/view/questions",
		name: "questions",
		component: QuestionView
	}, {
		path: "/view/friends",
		name: "friends",
		component: FriendView
	}]
}];

export default new VueRouter({
	mode: "history",
	routes
});