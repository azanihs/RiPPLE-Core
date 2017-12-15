import { ILink } from "../interfaces/models";

export function getLinks(): ILink[] {
    const profileLink: ILink = {
        text: "Profile",
        href: "",
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
        href: "",
        icon: "widgets",
        submenu: [{
            text: "Overview",
            href: "/admin"
        }, {
            text: "Consent Form",
            href: "/admin/consent"
        }, {
            text: "Reported Questions",
            href: "/admin/reported"
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
