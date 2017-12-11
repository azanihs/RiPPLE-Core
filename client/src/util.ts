import Vue from "vue";
import { ILink, INotification } from "./interfaces/models";

// From https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript/901144#901144
export function getParameterByName(name: string, url: string) {
    name = name.replace(/[\[\]]/g, "\\$&");
    let regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)");
    let results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return "";
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

export function getLinks(): ILink[] {
    const profileLink: ILink = {
        text: "Profile",
        href: "/",
        icon: "widgets",
        submenu: [{
            text: "Overview",
            href: "/"
        }, {
            text: "Engagement",
            href: "/profile/engagement"
        }, {
            text: "Competencies",
            href: "/profile/competencies"
        }, {
            text: "Connections",
            href: "/profile/connections"
        }, {
            text: "Achievements",
            href: "/profile/achievements"
        }, {
            text: "Notifications",
            href: "/profile/notifications"
        }, {
            text: "Consent",
            href: "/profile/consent"
        }]
    };
    const adminLink: ILink = {
        text: "Admin",
        href: "/admin",
        icon: "widgets",
        submenu: [{
            text: "Overview",
            href: "/admin"
        }, {
            text: "Consent Form",
            href: "/admin/consent"
        }]
    };
    const leaderLink: ILink = {
        text: "Leaders",
        href: "/view/leaderboard",
        icon: "assignment"
    };

    const questionLink: ILink = {
        text: "Questions",
        href: "/question/answer",
        icon: "question_answer",
        submenu: [{
            text: "Answer",
            href: "/question/answer"
        }, {
            text: "Create",
            href: "/question/create"
        }]
    };
    const connectLink: ILink = {
        text: "Connect",
        href: "/view/peers",
        icon: "group"
    };

    return [adminLink, profileLink, questionLink, connectLink, leaderLink];
}

const _bus = new Vue();

export const NEW_QUEUE_ITEM = "NEW_QUEUE_ITEM";

export function addEventsToQueue(items: INotification[]) {
    items.forEach(x => {
        _bus.$emit(NEW_QUEUE_ITEM, x);
    });
}

export function getBus() {
    return _bus;
}
