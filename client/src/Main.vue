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
                @click="toggleSideNav(undefined)">
                <md-icon>{{menuIcon}}</md-icon>
            </md-button>
        </md-layout>
        <md-layout ref="sidenavContainer"
            class="sideNavContainer"
            :class="pageSize"
            md-hide-xsmall
            md-hide-small>
                <user-container
                    :user="user"
                    :course="course"
                    @changeUser="updateUser"
                    @changeCourse="updateCourse"></user-container>
            <ul>
                <li v-for="link in links"
                    :key="link.href">
                    <router-link :to="link.href"
                        :class="submenuClassNames(link)"
                        @click.native="toggleSideNav(link)"
                        class="md-button routerLink">
                        <span>{{ link.text }}</span>
                        <md-icon>{{link.icon}}</md-icon>
                        <md-ink-ripple></md-ink-ripple>
                    </router-link>
                    <div v-if="link == currentlyOpenMenu || (link.submenu && link.submenu.indexOf(currentlyOpenMenu) >= 0)">
                            <li v-for="submenuLink in link.submenu"
                                :key="submenuLink.href">
                                <router-link :to="submenuLink.href"
                                    @click.native="keepProfileActive()"
                                    class ="profileSubmenu md-button routerLink">
                                    <span>{{ submenuLink.text }}</span>
                                </router-link>
                            </li>
                        </div>
                    </div>
                </li>
            </ul>
        </md-layout>
        <md-layout class="pageContent"
            :class="pageSize">
            <router-view></router-view>
        </md-layout>
        <global-notification></global-notification>
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

.profileSubmenu{
    background-color: #18181b;
    font-size: 0.8em;
    color: #fff;
    padding: 0px 20px !important;
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

.submenu-active {
    background-color: #1d323a;
    color: #f2f2f2;
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
    z-index: 10;
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

.router-link-exact-active.router-link-active:not(.has-submenu),
.router-link-exact-active.router-link-active:hover:not(.has-submenu){
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
import { Vue, Component, Prop, p, Lifecycle } from "av-ts";
import { ILink, User, Course, CourseUser } from "./interfaces/models";
import { getLinks } from "./util";

// Special case where main.vue needs to refresh application
import UserRepository from "./repositories/UserRepository";
import UserService from "./services/UserService";
import Fetcher from "./services/Fetcher";

import UserContainer from "./components/UserContainer.vue";
import GlobalNotification from "./GlobalNotification.vue";

@Component({
    components: {
        GlobalNotification,
        UserContainer
    }
})
export default class Main extends Vue {
    @Prop path = p<string>({
        required: true
    });

    courseRoles: string[] = [];
    pUser: User | undefined = undefined;
    pCourse: Course| undefined = undefined;
    pMenuLinks: ILink[] = getLinks();

    menuIcon = "menu";
    mobileMode = false;
    pageTitle = "";
    activeSubmenu = false;

    get user() {
        return this.pUser;
    }

    updateUser(newUser: User | undefined) {
        this.pUser = newUser;
    }

    updateCourseUser(courseUser: CourseUser) {
        this.updateUser(courseUser.user);
        this.courseRoles = courseUser.roles;

        if (this.pCourse === undefined) {
            this.pCourse = courseUser.course;
        }
    };

    get links() {
        return this.pMenuLinks;
    }

    get pageSize() {
        return this.mobileMode ? "mobilePage" : "largePage";
    }

    resized() {
        const sideNav = (this.$refs.sidenavContainer as Vue);
        const visible = (this.$refs.isVisible as Vue);
        if (!sideNav || !visible) {
            return;
        }

        const container = sideNav.$el;
        const isVisible = visible.$el;
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
        // Fix links
        if (this.course !== undefined && this.courseRoles.indexOf("Instructor") >= 0) {
            const profileLinkIndex = this.pMenuLinks.findIndex(x => x.href == "/");
            if (profileLinkIndex >= 0) {
                this.pMenuLinks.splice(profileLinkIndex, 1);
                this.$router.push("admin");
            }
        } else {
            const adminLinkIndex = this.pMenuLinks.findIndex(x => x.href == "/admin");
            if (adminLinkIndex >= 0) {
                this.pMenuLinks.splice(adminLinkIndex, 1);
            }
        }

        this.currentlyOpenMenu = this.pMenuLinks[0];
        Fetcher.get(UserService.getLoggedInUser)
            .on(this.updateCourseUser);
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
            .off(this.updateCourseUser);

        window.removeEventListener("resize", this.resized);
    }

    get course() {
        return this.pCourse;
    }

    updateCourse(newCourse: Course) {
        let oldCourseCode: string | undefined = undefined;
        if (this.pCourse && this.pCourse.courseCode) {
            oldCourseCode = this.pCourse.courseCode;
        }

        if (newCourse === undefined) return;

        this.pCourse = newCourse;
        UserRepository.authenticate(newCourse.courseCode)
            .then(_ => {
                const preserveCache = !(oldCourseCode == newCourse.courseCode);
                Fetcher.forceUpdate(preserveCache);
            });
    }

    currentlyOpenMenu: ILink | undefined = undefined;

    toggleSubmenu(link: ILink) {
        this.currentlyOpenMenu = link;
    }

    toggleSideNav(link: ILink | undefined) {
        if (link !== undefined) {
            this.toggleSubmenu(link);
        }

        if (this.mobileMode) {
            this.updatePageName();
            const menuButton = (this.$refs["menuButton"] as Vue).$el;
            const container = (this.$refs.sidenavContainer as Vue).$el;
            const linkHasSubmenu = link !== undefined && link.submenu !== undefined;
            if (!container.style.transform || linkHasSubmenu) {
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

    keepProfileActive() {
        this.activeSubmenu = true;
        if (this.mobileMode) {
            const container = (this.$refs.sidenavContainer as Vue).$el;
            container.style.transform = null;
            this.menuIcon = "menu";
        }
    }

    submenuClassNames(link: ILink) {
        if (link.submenu !== undefined) {
            return "has-submenu";
        }
    }

}
</script>
