<template>
    <md-layout>
        <md-layout class="offset"
            ref="isVisible"
            md-hide-medium-and-up></md-layout>
        <md-layout md-hide-medium-and-up
            class="menuContainer">
            <h2>{{ pageTitle }}</h2>
        </md-layout>
        <md-layout md-hide-medium-and-up>
            <md-button class="md-icon-button menuButton"
                ref="menuButton"
                @click="toggleSideNav">
                <md-icon>{{menuIcon}}</md-icon>
            </md-button>
        </md-layout>
        <md-layout ref="sidenavContainer"
            class="sideNavContainer"
            :class="pageSize"
            md-hide-xsmall
            md-hide-small>
            <div class="profileContainer">
                <div class="imageContainer">
                    <img :src="personalAvatar" />
                </div>
                <h5>{{userFullName}}</h5>
                <select v-model="course">
                    <option v-for="enrolledCourse in userCourses"
                        :key="enrolledCourse.courseCode"
                        :value="enrolledCourse">
                        {{enrolledCourse.courseCode}}
                    </option>
                </select>
            </div>
            <ul>
                <li v-for="link in links"
                    :key="link.href">
                    <router-link :to="link.href"
                        @click.native="toggleSideNav"
                        class="md-button routerLink">
                        <span>{{ link.text }}</span>
                        <md-icon>{{link.icon}}</md-icon>
                        <md-ink-ripple></md-ink-ripple>
                    </router-link>
                </li>
            </ul>
        </md-layout>
        <md-layout class="pageContent"
            :class="pageSize">
            <router-view></router-view>
        </md-layout>
    </md-layout>
</template>

<style scoped>
.menuContainer {
    position: fixed;
    left: 0px;
    top: 0px;
    width: 100%;
    height: 54px;
    background-color: #fff;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2), 0 2px 2px rgba(0, 0, 0, 0.14),
        0 3px 1px -2px rgba(0, 0, 0, 0.12);

    justify-content: flex-end;
}

.menuContainer h2 {
    padding-right: 16px;
    color: #999;
}

.menuButton {
    margin: 8px !important;
    background-color: #1d323a !important;
    color: #f2f2f2 !important;
    position: fixed;
    left: 0px;
    top: 0px;
}

.offset {
    height: 54px;
    min-width: 100%;
}

.sideNavContainer {
    background-color: #1d323a;
    color: #f2f2f2;
    height: 100%;
    display: block !important;
    transform: translate3d(-100%, 0, 0);
    transition: all 250ms ease;
    position: fixed;
    left: 0px;
    top: 0px;
    width: 16.25%;
}

.sideNavContainer.mobilePage {
    width: auto;
    min-width: 170px;
}

.pageContent {
    width: 82.5%;
    margin-left: 16.875%;
    margin-right: 0.625%;
}

.pageContent.mobilePage {
    margin-left: 1.25%;
    margin-right: 1.25%;
    min-width: 97.5%;
    flex: 0 1 97.5%;
}

.profileContainer {
    text-align: center;
    margin: auto;
    margin-bottom: 1em;
}

.profileContainer .imageContainer {
    width: 100px;
    height: 100px;
    padding: 10px;
    margin: auto;
}

.imageContainer img {
    width: 100%;
    height: 100%;
    border-radius: 100%;
}

.profileContainer h5 {
    font-weight: normal;
    font-size: 1em;
    margin: 0px auto;
}

.profileContainer h4 {
    font-size: 1em;
    margin: 0px;
    padding: 0px;
    color: #aaa;
}

ul {
    margin: 0px;
    padding: 0px;
    width: 100%;
}

ul > li {
    list-style: none;
    padding: 0px;
    margin: 0px !important;
}

.routerLink {
    width: 100%;
    margin: 0px;
    display: flex;
    flex: 1;
    justify-content: space-between;
    padding: 5px 20px;
    border-radius: 0px;
    border-top: 1px solid #274550;
}

.routerLink:last-child {
    border-bottom: 1px solid #274550;
}

.routerLink > i {
    margin-left: 0px;
    margin-right: 0px;
    color: #4d656d;
}

a.routerLink,
a.routerLink:hover {
    text-decoration: none !important;
}

.router-link-exact-active.router-link-active .linkButton.md-icon-button {
    border-radius: 0px;
    margin: 0px;
}

.router-link-exact-active.router-link-active,
.router-link-exact-active.router-link-active:hover {
    /* Sets the background colour of the currently selected item */
    background-color: #ffffff !important;
    color: #111 !important;
}
</style>

<style>
label {
    cursor: pointer;
}
</style>
<script lang="ts">
import { Vue, Component, Prop, Lifecycle } from "av-ts";
import { User, Course, CourseUser } from "./interfaces/models";

// Special case where main.vue needs to refresh application
import UserRepository from "./repositories/UserRepository";
import UserService from "./services/UserService";
import Fetcher from "./services/Fetcher";

@Component()
export default class Main extends Vue {
    @Prop path;

    courseRoles: string[] = [];
    pUser: User = undefined;
    pCourse: Course = undefined;

    pCourses = [];

    updateUser(courseUser: CourseUser) {
        this.pUser = courseUser.user;
        this.courseRoles = courseUser.roles;
        if (this.pCourse === undefined) {
            this.pCourse = courseUser.course;
        }
    };

    get personalAvatar() {
        if (this.pUser !== undefined) {
            return this.pUser.image;
        }

        return "";
    }

    get userFullName() {
        if (this.pUser === undefined) {
            return "Loading...";
        }

        return this.pUser.name;
    }

    updateCourses(newCourses) {
        this.pCourses = newCourses;
        if (this.pCourse === undefined && newCourses.length > 0) {
            this.pCourse = newCourses[0];
        }
    }

    get userCourses() {
        return this.pCourses;
    }

    menuIcon = "menu";
    mobileMode = false;
    pageTitle = "";

    get links() {
        const profileLink = {
            text: "Profile",
            href: "/",
            icon: "widgets"
        };
        const adminLink = {
            text: "Admin",
            href: "/admin",
            icon: "widgets"
        };
        const leaderLink = {
            text: "Leaders",
            href: "/view/leaderboard",
            icon: "assignment"
        };

        const baseLinks = [{
            text: "Answer",
            href: "/view/questions",
            icon: "lightbulb_outline"
        }, {
            text: "Connect",
            href: "/view/peers",
            icon: "group"
        }, {
            text: "Author",
            href: "/view/author",
            icon: "attach_file"
        }];

        if (this.course !== undefined && this.courseRoles.indexOf("Instructor") >= 0) {
            baseLinks.unshift(adminLink);
            this.$router.push("admin");
        } else {
            baseLinks.unshift(profileLink);
            baseLinks.push(leaderLink);
        }
        return baseLinks;
    }

    get pageSize() {
        return this.mobileMode ? "mobilePage" : "largePage";
    }

    resized() {
        const container = (this.$refs.sidenavContainer as any).$el as HTMLElement;
        const isVisible = (this.$refs.isVisible as any).$el as HTMLElement;
        if (window.getComputedStyle(isVisible).display !== "none") {
            this.mobileMode = true;
            this.menuIcon = "menu";
            container.style.transform = null;
        } else {
            this.mobileMode = false;
            this.menuIcon = "menu";
            container.style.transform = "translate3d(0,0,0)";
        }
    }

    updatePageName() {
        const link = this.links.find(x => x.text.toLowerCase() == this.path);
        if (link !== undefined) {
            this.pageTitle = link.text + " Page";
        }
    }

    @Lifecycle
    created() {
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateUser);
        Fetcher.get(UserService.getUserCourses)
            .on(this.updateCourses);
    }

    @Lifecycle
    mounted() {
        window.addEventListener("resize", this.resized);
        this.updatePageName();
        this.resized();
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getLoggedInUser)
            .off(this.updateUser);

        window.removeEventListener("resize", this.resized);
    }

    get course() {
        return this.pCourse;
    }

    set course(newCourse) {
        let oldCourseCode = undefined;
        if (this.pCourse && this.pCourse.courseCode) {
            oldCourseCode = this.pCourse.courseCode;
        }

        if (newCourse === undefined) return;

        this.pCourse = newCourse;
        UserRepository.authenticate(newCourse.courseCode)
            .then(newToken => {
                const preserveCache = !(oldCourseCode == newCourse.courseCode);
                Fetcher.forceUpdate(preserveCache);
            });
    }

    toggleSideNav() {
        if (this.mobileMode) {
            this.updatePageName();
            const menuButton = (this.$refs["menuButton"] as any).$el as HTMLElement;
            const container = (this.$refs.sidenavContainer as any).$el as HTMLElement;

            if (!container.style.transform) {
                container.style.transform = "translate3d(0,0,0)";
                container.style.opacity = "1";
                menuButton.style.color = "#f2f2f2";
                this.menuIcon = "close";
            } else {
                menuButton.style.color = "#222";
                container.style.transform = null;
                container.style.display = null;
                this.menuIcon = "menu";
            }
        }
    }
}
</script>
