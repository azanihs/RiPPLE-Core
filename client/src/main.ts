import Vue from "vue";
import Router from "./routes";
import VueMaterial from "vue-material";
import "flatpickr/dist/flatpickr.css";
import "./tinymce";

import "vue-material/dist/vue-material.css";
import "./style/style.css";

import UserRepository from "./repositories/UserRepository";
import { getParameterByName } from "./util";

// Global scoped addons
Vue.use(VueMaterial);

Vue.material.registerTheme("spinner", {
    primary: "grey",
    accent: "grey",
    warn: "grey",
    background: "grey"
});

// Fetch User token from server
new Promise(resolve => {
    const token = getParameterByName("token", window.location.href);
    const courseCode = getParameterByName("course_code", window.location.href);
    if (token && courseCode) {
        // UserRepository.setCurrentCourse(courseCode);
        UserRepository.setCurrentToken(token);
        resolve(UserRepository.authenticate(courseCode));
    } else {
        resolve(UserRepository.authenticate());
    }
})
    .catch(err => {
        if (err instanceof Response) {
            document.body.innerHTML = `<h1>Could not authenticate with server</h1><pre>
                Message: ${err.statusText}
                Code: ${err.status}
                url: ${err.url}
            </pre>`;
        // Re-throw error to get it into the console and prevent the next .then(() => ...)
        } else {
            document.body.innerHTML = `<h1>Could not authenticate with server</h1><pre>
                ${err}
            </pre>`;
        }
        throw err;
    })
    .then(_ => {
        const appContainer = document.createElement("div");
        appContainer.id = "main";
        appContainer.innerHTML = "<router-view></router-view>";
        document.body.appendChild(appContainer);
        new Vue({
            el: "#main",
            router: Router
        });
    });

