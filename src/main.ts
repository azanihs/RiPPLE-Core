import UserRepository from "./repositories/UserRepository";

import Vue from "vue";
import Router from "./routes";
import VueMaterial from "vue-material";
import "vue-material/dist/vue-material.css";

import "./style/style.css";

// Global scoped addons
Vue.use(VueMaterial);

Vue.material.registerTheme("spinner", {
    primary: "grey",
    accent: "grey",
    warn: "grey",
    background: "grey"
});

const appContainer = document.createElement("div");
appContainer.id = "main";
appContainer.innerHTML = "<router-view></router-view>";
document.body.appendChild(appContainer);

// Fetch User token from server
UserRepository.authenticate()
    .catch(err => {
        document.body.innerHTML = `<h1>Could not authenticate with server</h1><pre>
            Message: ${err.statusText}
            Code: ${err.status}
            url: ${err.url}
        </pre>`;
    })
    .then(x => {
        new Vue({
            el: "#main",
            router: Router
        });
    });

