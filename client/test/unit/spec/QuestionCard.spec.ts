import Vue from "vue";
import VueRouter from "vue-router";
import VueMaterial from "vue-material";

import "vue-material/dist/vue-material.css";

import { Question, User, Distractor } from "../../../src/interfaces/models";
import QuestionPreview from "../../../src/components/questions/QuestionPreview.vue";

import { assert } from "chai";

Vue.use(VueMaterial);
Vue.use(VueRouter);

const router = new VueRouter({
    mode: "history",
    routes: []
});

const peer = id => {
    const peer: User = {
        id: id,
        name: "Test User",
        bio: "Test Bio",

        proficiencies: ["SSL"],
        image: "",
        availableTime: new Date(),

        connections: []
    };
    return peer;
};

const optionA: Distractor = {
    id: 0,
    content: "",
    isCorrect: false,
    response: "A"
};
const optionB: Distractor = {
    id: 1,
    content: "",
    isCorrect: true,
    response: "B"
};

const basicQuestion: Question = {
    id: 1,
    responses: [{
        author: peer(1),
        upVotes: 2,
        solution: 0,
        content: ""
    }],
    difficulty: 1,
    quality: 1,
    solution: optionB,
    distractors: [optionA, optionB],
    explanation: "",
    content: "Basic question content",
    topics: [{ id: 1, name: "Topic 1" }, { id: 2, name: "Topic 2" }]
};

describe("QuestionCard.vue", () => {
    beforeEach(() => {
        let main = document.getElementById("app");
        if (main) {
            main.parentElement.removeChild(main);
        }
        main = document.createElement("div");
        main.id = "app";
        document.body.appendChild(main);

        let mountPoint = document.createElement("div");
        mountPoint.id = "mountPoint";
        main.appendChild(mountPoint);
    });

    it("Correctly renders difficulty", () => {
        const testData = [0, 3, 4, 7, 10];
        const runTest = expected => {
            const testQuestion: Question = Object.assign({}, basicQuestion);
            testQuestion.difficulty = expected;
            const mountPoint = document.getElementById("mountPoint");
            let vm = new QuestionPreview({
                router: router
            });
            vm.data = testQuestion;
            vm.$mount(mountPoint);
            return vm.$nextTick()
                .then(() => {
                    const difficulty = vm.$el
                        .querySelector(".rightPanel>div:nth-child(2) span");
                    assert.equal((difficulty as HTMLElement).innerText.trim(), expected);
                });
        };
        return testData.reduce((chain, testCase) =>
            chain.then(runTest.bind(null, testCase)), runTest(testData.shift()));
    });

    it("Correctly renders quality", () => {
        const testData = [0, 3, 4, 7, 10];
        const runTest = expected => {
            const testQuestion: Question = Object.assign({}, basicQuestion);
            testQuestion.quality = expected;
            const mountPoint = document.getElementById("mountPoint");
            let vm = new QuestionPreview({
                router: router
            });
            vm.data = testQuestion;
            vm.$mount(mountPoint);
            return Vue.nextTick()
                .then(() => {
                    const quality = vm.$el
                        .querySelector(".rightPanel>div:nth-child(3) span");
                    assert.equal((quality as HTMLElement).innerText.trim(), expected);
                    return;
                });
        };
        return testData.reduce((chain, testCase) =>
            chain.then(runTest.bind(null, testCase)), runTest(testData.shift()));
    });
});
