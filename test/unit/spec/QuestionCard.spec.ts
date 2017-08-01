import Vue from "vue";
import VueRouter from "vue-router";
import VueMaterial from "vue-material";

import "vue-material/dist/vue-material.css";

import { Question, Peer } from "../../../src/interfaces/models";
import QuestionCard from "../../../src/components/questions/QuestionCard.vue";

import { assert } from "chai";

Vue.use(VueMaterial);
Vue.use(VueRouter);

const router = new VueRouter({
    mode: "history",
    routes: []
});

const peer = id => {
    const peer: Peer = {
        id: id,
        name: "Test User",
        bio: "Test Bio",

        proficiencies: ["SSL"],
        image: "",
        availableTimes: []
    };
    return peer;
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
    difficultyRepresentation: "",
    solution: 0,
    possibleAnswers: [{
        id: 0,
        content: ""
    }, {
        id: 1,
        content: ""
    }],
    explanation: "",
    content: "Basic question content",
    topics: ["Topic 1", "Topic 2"],
    images: []
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
        const testData = [{
            value: 0,
            expected: "Easy"
        }, {
            value: 3,
            expected: "Easy"
        }, {
            value: 4,
            expected: "Medium"
        }, {
            value: 7,
            expected: "Hard"
        }, {
            value: 10,
            expected: "Hard"
        }];
        const runTest = data => {
            const hardQuestion: Question = Object.assign({}, basicQuestion);
            hardQuestion.difficulty = data.value;
            const mountPoint = document.getElementById("mountPoint");
            let vm = new QuestionCard({
                router: router
            });
            vm.data = hardQuestion;
            vm.$mount(mountPoint);
            return Vue.nextTick()
                .then(() => {
                    const difficulty = vm.$children[0].$el.querySelector(".difficulty") as HTMLElement;
                    assert.equal(difficulty.innerText.replace(/\s{2,}/, " ").trim(), data.expected + " school");
                    assert.equal(vm.getDifficultyText(data.value).trim(), data.expected);
                    return;
                });
        };
        return testData.reduce((chain, testCase) =>
            chain.then(runTest.bind(null, testCase)), runTest(testData.shift()));
    });

    it("Correctly renders quality", () => {
        const testData = [{
            value: 0,
            expected: new Array(5).fill("star_border")
        }, {
            value: 3,
            expected: ["star", "star_half", "star_border", "star_border", "star_border"]
        }, {
            value: 4,
            expected: ["star", "star", "star_border", "star_border", "star_border"]
        }, {
            value: 7,
            expected: ["star", "star", "star", "star_half", "star_border"]
        }, {
            value: 10,
            expected: new Array(5).fill("star")
        }];
        const runTest = data => {
            const hardQuestion: Question = Object.assign({}, basicQuestion);
            hardQuestion.difficulty = data.value;
            const mountPoint = document.getElementById("mountPoint");
            let vm = new QuestionCard({
                router: router
            });
            vm.data = hardQuestion;
            vm.$mount(mountPoint);
            return Vue.nextTick()
                .then(() => {
                    const quality = vm.$children[0].$el.querySelector(".quality") as HTMLElement;
                    // One extra child because of tooltip
                    assert.equal(quality.childNodes.length, data.expected.length + 1);
                    assert.deepEqual(vm.getStarIcons(data.value), data.expected);
                });
        };

        return testData.reduce((chain, testCase) => chain.then(runTest.bind(null, testCase)),
            runTest(testData.shift()));
    });
});
