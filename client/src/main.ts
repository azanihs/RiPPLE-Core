import UserRepository from "./repositories/UserRepository";

import Vue from "vue";
import Router from "./routes";
import VueMaterial from "vue-material";
import VueTinymce from "vue-tinymce";

import "flatpickr/dist/flatpickr.css";

import "./tinymce";

import "vue-material/dist/vue-material.css";
import "./style/style.css";

// From https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript/901144#901144
function getParameterByName(name, url) {
    name = name.replace(/[\[\]]/g, "\\$&");
    let regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)");
    let results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return "";
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

// Global scoped addons
Vue.use(VueMaterial);
Vue.use(VueTinymce);

Vue.material.registerTheme("spinner", {
    primary: "grey",
    accent: "grey",
    warn: "grey",
    background: "grey"
});

class AuthenticationError {
    constructor(public statusText: string, public status: string, public url: string) {
    }
}
// Fetch User token from server
new Promise((resolve, reject) => {
    const token = getParameterByName("token", window.location.href);
    const courseCode = getParameterByName("course_code", window.location.href);
    if (token && courseCode) {
        UserRepository.setCurrentCourse(courseCode);
        UserRepository.setCurrentToken(token);
        resolve(UserRepository.authenticate(courseCode));
    } else {
        resolve(UserRepository.authenticate());
    }
})
    .catch(err => {
        document.body.innerHTML = `<h1>Could not authenticate with server</h1><pre>
                Message: ${err.statusText}
                Code: ${err.status}
                url: ${err.url}
            </pre>`;
    })
    .then(x => {
        const appContainer = document.createElement("div");
        appContainer.id = "main";
        appContainer.innerHTML = "<router-view></router-view>";
        document.body.appendChild(appContainer);
        new Vue({
            el: "#main",
            router: Router
        });
    });

