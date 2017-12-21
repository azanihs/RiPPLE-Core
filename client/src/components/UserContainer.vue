<template>
    <div class="profileContainer">
        <div class="imageContainer" @click="openImagePicker"
        :class = "{'mobileStyle': mobileMode}">
            <img :src="personalAvatar" />
            <md-icon v-if="personalAvatar == undefined && !mobileMode" class="md-size-4x">add_a_photo</md-icon>
            <md-icon v-else-if = "!mobileMode" class="md-size-2x">edit</md-icon>
        </div>
        <h5>{{userFullName}}</h5>
        <select v-model="currentCourse">
            <option v-for="enrolledCourse in courses"
                :key="enrolledCourse.courseCode"
                :value="enrolledCourse">
                {{enrolledCourse.courseCode}}
            </option>
        </select>
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

.mobileStyle {
    cursor: default !important;
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
import { Vue, Component, Lifecycle, Prop, p, Mixin as mixin } from "av-ts";
import { ICourseUser, IUser, ICourse } from "../interfaces/models";
import { addEventsToQueue } from "../util";
import UserService from "../services/UserService";
import ImageService from "../services/ImageService";
import responsiveMixin from "./../responsiveMixin";
import Fetcher from "../services/Fetcher";

@Component
export default class UserContainer extends mixin(responsiveMixin, Vue) {
    @Prop user = p<IUser | undefined>({
        required: false
    });
    @Prop course = p<ICourse | undefined>({
        required: false
    });

    pCourse: ICourse | undefined = undefined;
    pCourses: ICourse[] = [];

    set currentCourse(newCourse: ICourse | undefined) {
        this.pCourse = newCourse;
        this.$emit("changeCourse", newCourse);
    }

    get currentCourse() {
        return this.course || this.pCourse;
    }

    updateCourses(newCourses: ICourse[]) {
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
        return (e: Event) => {
            const newImages = (e.target as HTMLInputElement).files || [];
            if (newImages.length == 0) {
                // Snackbar err
                document.body.removeChild(input);
                this.showMessage("No file selected");
            } else {
                ImageService.fileToBase64EncodeString(newImages[0])
                    .then(file => UserService.updateUserImage({
                        newImage: (file as any).base64 as string
                    }))
                    .then((user: IUser) => {
                        this.$emit("changeUser", user);
                        UserService.getLoggedInUser()
                            .then((cu: ICourseUser) => {
                                this.$emit("changeUser", cu.user);
                            });
                        this.showMessage("Profile image changed", "done");
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
        if (!this.mobileMode) {
            const input = document.createElement("input");
            input.type = "file";
            input.addEventListener("change", (e: Event) => this.handleImageChange(input)(e));

            document.body.appendChild(input);
            input.dispatchEvent(new MouseEvent("click", {
                bubbles: false
            }));
        }
    }

    showMessage(message: string, icon: string = "error") {
        addEventsToQueue([{
            name: "Image Upload",
            description: message,
            icon: icon
        }]);
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
