<template>
    <md-layout>
        <div v-if="mobileMode && sideMenuIsOpen"
        class="dimOverlay"
        @click="hideSideBar()"></div>
        <md-layout class="offset"
            ref="isVisible"
            md-hide-medium-and-up></md-layout>
        <md-layout md-hide-medium-and-up
            class="menuContainer">
            <h2>{{ pageTitle }}</h2>
        </md-layout>
        <md-layout md-hide-medium-and-up>
            <md-button class="md-icon-button menuButton"
                :class="menuButtonClass"
                @click="toggleSideNav(undefined)">
                <md-icon class="closeIcon">{{menuIcon}}</md-icon>
            </md-button>
        </md-layout>
        <md-layout ref="sidenavContainer"
            class="sideNavContainer"
            :class="pageSize"
            md-hide-xsmall
            md-hide-small>
                <md-button v-if="mobileMode" class="md-icon-button closeButton"
                    :class="menuButtonClass"
                    @click="toggleSideNav(undefined)">
                        <md-icon>{{closeIcon}}</md-icon>
                </md-button>
                <user-container
                    :user="user"
                    :course="course"
                    @changeUser="updateUser"
                    @changeCourse="updateCourse">
                </user-container>
            <ul class="sideNavList">
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
                        <transition-group name="slide" tag="ul"
                            appear
                            appear-class="slide-appear-class"
                            appear-active-class="slide-appear-active-class">
                            <li v-for="submenuLink in link.submenu"
                                :key="submenuLink.href">
                                <router-link :to="submenuLink.href"
                                    @click.native="keepProfileActive(submenuLink)"
                                    class ="profileSubmenu md-button routerLink">
                                    <span>{{ submenuLink.text }}</span>
                                </router-link>
                            </li>
                        </transition-group>
                    </div>
                </li>
            </ul>
        </md-layout>
        <md-layout class="pageContent"
            :class="pageSize">
            <router-view :key="$route.fullPath"></router-view>
        </md-layout>
        <global-notification></global-notification>
        <page-loader :condition="loading"></page-loader>
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
    z-index: 2;
}

@media only screen and (max-device-height: 480px) and (orientation: landscape) {
        .sideNavList {
        overflow-y: scroll;
        max-height: 60%;
        border-top-style: solid;
        border-top-color: #999;
        border-top-width: 3px;
    }
}


.slide-appear-active-class {
    opacity: 1;
    max-height: 36px;
    transition: all 0.3s;
}

.slide-appear-class {
    opacity: 0;
    max-height: 0px;
}


.dimOverlay {
    position:fixed;
    padding:0;
    margin:0;
    top:0;
    left:0;
    width: 100%;
    height: 100%;
    background:rgba(0,0,0,0.5);
    z-index: 5;
}

.profileSubmenu{
    background-color: #18181b;
    font-size: 0.8em;
    color: #fff;
    padding: 0px 20px !important;
}

.profileSubmenu.md-button:hover:not([disabled]):not(.md-raised) {
    background-color: rgba(153, 153, 153, 0.5);
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
    z-index: 2;
}

.closeButton {
    color: #f2f2f2 !important;
    right:0px !important;
    left: initial;
    position: fixed;
    right: 0px;
    top: 0px;
    z-index: 2;
    margin: 2px 2px !important;
}

.closeButton > .md-icon {
    margin: unset !important;
    left:initial !important;
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
    z-index: 0;
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

.expanded {
    transform: translate3d(0,0,0);
    opacity: 1;
}

</style>

<style>
label {
    cursor: pointer;
}
</style>
<script lang="ts">
import { Vue, Component, Prop, p, Lifecycle } from "av-ts";
import { ILink, IUser, ICourse, ICourseUser } from "./interfaces/models";
import { getLinks } from "./routes/links";

// Special case where main.vue needs to refresh application
import UserRepository from "./repositories/UserRepository";
import UserService from "./services/UserService";
import Fetcher from "./services/Fetcher";

import UserContainer from "./components/UserContainer.vue";
import PageLoader from "./components/util/PageLoader.vue";
import GlobalNotification from "./GlobalNotification.vue";

@Component({
    components: {
        GlobalNotification,
        UserContainer,
        PageLoader
    }
})
export default class Main extends Vue {
    @Prop path = p<string>({
        required: true
    });

    courseRoles: string[] = [];
    pUser: IUser | undefined = undefined;
    pCourse: ICourse| undefined = undefined;
    pMenuLinks: ILink[] = getLinks();
    currentlyOpenMenu: ILink | undefined = undefined;

    menuIcon = "menu";
    closeIcon = "close";
    sideMenuIsOpen = false;
    mobileMode = false;
    pageTitle = "";
    activeSubmenu = false;
    loading = false;

    get user() {
        return this.pUser;
    }

    updateUser(newUser: IUser | undefined) {
        this.pUser = newUser;
    }

    updateCourseUser(courseUser: ICourseUser) {
        this.updateUser(courseUser.user);
        this.courseRoles = courseUser.roles;

        if (this.pCourse === undefined) {
            this.pCourse = courseUser.course;
        }

        const _linkCopy = this.pMenuLinks.slice();
        // Fix links
        if (this.course !== undefined && this.courseRoles.indexOf("Instructor") >= 0) {
            const profileLinkIndex = _linkCopy.findIndex(x => x.text == "Profile");
            if (profileLinkIndex >= 0) {
                _linkCopy.splice(profileLinkIndex, 1);
            }

            // Only redirect when no menu is open
            if (this.currentlyOpenMenu === undefined) {
                this.currentlyOpenMenu = this.pMenuLinks[0];
                this.$router.push("/admin");
            }
        } else {
            const adminLinkIndex = _linkCopy.findIndex(x => x.text == "Admin");
            if (adminLinkIndex >= 0) {
                _linkCopy.splice(adminLinkIndex, 1);
                if (this.currentlyOpenMenu === undefined) {
                    const questionLinkIndex = _linkCopy.findIndex(x => x.text == "Questions");
                    if (questionLinkIndex == -1) {
                        throw new Error("Missing question links.");
                    }
                    this.currentlyOpenMenu = _linkCopy[questionLinkIndex].submenu![0];
                }
            }
        }

        this.pMenuLinks = _linkCopy;
    };

    get links() {
        return this.pMenuLinks;
    }

    get pageSize() {
        return {
            "mobilePage": this.mobileMode,
            "largePage": !this.mobileMode,
            "expanded": this.sideMenuIsOpen
        };
    }
    get menuButtonClass() {
        return {
            "highlighted": this.sideMenuIsOpen
        };
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
            container.style.transform = null;
        } else {
            this.mobileMode = false;
            container.style.transform = "translate3d(0,0,0)";
        }
    }

    updatePageName() {
        if (this.currentlyOpenMenu !== undefined) {
            if (this.currentlyOpenMenu.href != "") {
                this.pageTitle = this.currentlyOpenMenu.text;
            } else if (this.currentlyOpenMenu.href == "") {
                this.pageTitle = this.path.charAt(0).toUpperCase() + this.path.slice(1);
            }
        }
    }

    @Lifecycle
    created() {
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

    updateCourse(newCourse: ICourse) {
        let oldCourseCode: string | undefined = undefined;
        if (this.pCourse && this.pCourse.courseCode) {
            oldCourseCode = this.pCourse.courseCode;
        }

        if (newCourse === undefined) return;

        this.pCourse = newCourse;
        this.loading = true;
        UserRepository.authenticate(newCourse.courseCode)
            .then(_ => {
                const preserveCache = !(oldCourseCode == newCourse.courseCode);
                Fetcher.forceUpdate(preserveCache)
                    .then(() => {
                        this.loading = false;
                    });
            });
    }

    toggleSubmenu(link: ILink) {
        this.currentlyOpenMenu = link;
        this.updatePageName();
    }

    toggleSideNav(link: ILink | undefined) {
        if (link !== undefined) {
            this.toggleSubmenu(link);
        }

        if (this.mobileMode) {
            this.updatePageName();
            const linkHasSubmenu = link !== undefined && link.submenu !== undefined;
            if (this.sideMenuIsOpen && linkHasSubmenu) {
                this.sideMenuIsOpen = true;
            } else if (this.sideMenuIsOpen && !linkHasSubmenu) {
                this.sideMenuIsOpen = false;
            } else {
                this.sideMenuIsOpen = true;
            }
        }
    }

    keepProfileActive(link: ILink) {
        this.activeSubmenu = true;
        this.toggleSideNav(link);
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

    hideSideBar() {
        this.sideMenuIsOpen = false;
    }

}
</script>
