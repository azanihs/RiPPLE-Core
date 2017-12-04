<template>
    <div class="profileContainer">
        <div class="imageContainer" @click="openImagePicker">
            <img :src="personalAvatar" />
            <md-icon v-if="personalAvatar == undefined" class="md-size-4x">add_a_photo</md-icon>
            <md-icon v-else class="md-size-2x">edit</md-icon>
        </div>
        <h5>{{userFullName}}</h5>
        <select v-model="currentCourse">
            <option v-for="enrolledCourse in courses"
                :key="enrolledCourse.courseCode"
                :value="enrolledCourse">
                {{enrolledCourse.courseCode}}
            </option>
        </select>
          <md-snackbar md-position="bottom center" ref="snackbar" :md-duration="6000">
                <span>{{errorMessage}}</span>
                <md-button class="md-primary" @click="$refs.snackbar.close()">Close</md-button>
        </md-snackbar>
    </div>
</template>

<style scoped>
.profileContainer {
    text-align: center;
    margin: auto;
    margin-bottom: 1em;
}

.imageContainer {
    width: 100px;
    height: 100px;
    padding: 10px;
    margin: auto;
    position: relative;
    cursor: pointer;
}

.imageContainer img {
    width: 100%;
    height: 100%;
    border-radius: 100%;
}
.imageContainer .md-icon {
    opacity: 0;
    position: absolute;
    top: 25%;
    left: 25%;
    transition: opacity 250ms ease;
}
.imageContainer:hover .md-icon {
    opacity: 1;
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
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import { CourseUser, User, Course } from "../interfaces/models";

import UserService from "../services/UserService";
import ImageService from "../services/ImageService";

import Fetcher from "../services/Fetcher";

@Component()
export default class UserContainer extends Vue {
    @Prop user = p<User | undefined>({
        required: false
    });
    @Prop course = p<Course | undefined>({
        required: false
    });

    pCourse: Course = undefined;
    pCourses: Course[] = [];
    errorMessage: string = "";

    set currentCourse(newCourse: Course) {
        this.pCourse = newCourse;
        this.$emit("changeCourse", newCourse);
    }

    get currentCourse() {
        return this.course || this.pCourse;
    }

    updateCourses(newCourses: Course[]) {
        this.pCourses = newCourses;
        if (this.pCourse === undefined && newCourses.length > 0) {
            this.pCourse = newCourses[0];
        }
    }

    get courses() {
        return this.pCourses;
    }

    get personalAvatar() {
        if (this.user !== undefined) {
            return this.user.image;
        }
        return "";
    }

    get userFullName() {
        if (this.user === undefined) {
            return "Loading...";
        }
        return this.user.name;
    }

    handleImageChange(input: HTMLInputElement) {
        return (e: MouseEvent) => {
            const newImages = (e.target as HTMLInputElement).files;
            if (newImages.length == 0) {
                // Snackbar err
                document.body.removeChild(input);
                this.showMessage("No file selected");
            } else {
                ImageService.fileToBase64EncodeString(newImages[0])
                    .then(file => UserService.updateUserImage({
                        newImage: (file as any).base64 as string
                    }))
                    .then((user: User) => {
                        this.$emit("changeUser", user);
                        UserService.getLoggedInUser()
                            .then((cu: CourseUser) => {
                                this.$emit("changeUser", cu.user);
                            });
                        this.showMessage("Profile image changed");
                        document.body.removeChild(input);
                    })
                    .catch(err => {
                        this.showMessage(err);
                        document.body.removeChild(input);
                    });
            }
        };
    }

    openImagePicker() {
        const input = document.createElement("input");
        input.type = "file";
        input.addEventListener("change", this.handleImageChange(input));

        document.body.appendChild(input);
        input.dispatchEvent(new MouseEvent("click", {
            bubbles: false
        }));
    }

    showMessage(message: string) {
        this.errorMessage = message;
        (this.$refs["snackbar"] as any).open();
    }

    @Lifecycle
    created() {
        Fetcher.get(UserService.getUserCourses)
            .on(this.updateCourses);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.getUserCourses)
            .off(this.updateCourses);
    }
}
</script>
