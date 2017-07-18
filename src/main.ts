import Vue from "vue";
import Router from "./routes";
import VueMaterial from "vue-material";
import "vue-material/dist/vue-material.css";

// Global scoped addons
Vue.use(VueMaterial);

Vue.material.registerTheme('spinner', {
    primary: 'grey',
    accent: 'grey',
    warn: 'grey',
    background: 'grey'
});

const appContainer = document.createElement("div");
appContainer.id = "main";
appContainer.innerHTML = "<router-view></router-view>";
document.body.appendChild(appContainer);

/* eslint-disable no-new */
new Vue({
    el: "#main",
    router: Router,
});
