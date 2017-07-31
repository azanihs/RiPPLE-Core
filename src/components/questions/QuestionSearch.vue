<template>
    <md-layout md-flex="100">
        <h2>Search </h2>
        <md-layout md-flex="100" class="header">
            <md-layout md-hide-xsmall md-hide-small md-hide-medium v-for="field in searchableFields" :key="field.displayName">
                <h3 v-if="field.sort" @click="field.sort">
                    <md-icon v-if="field.sort">{{reverseSortOrder ? "arrow_drop_down" : "arrow_drop_up" }}</md-icon>
                    {{ field.displayName }}
                </h3>
                <h3 v-else>
                    {{ field.displayName }}
                </h3>
                <select v-if="field.type == 'select'" @change="field.search">
                    <option value=""></option>
                    <option v-for="option in field.options" :key="option" :value="option">{{ option }}</option>
                </select>
                <input v-else-if="field.type == 'text'" @change="field.search" type="text"></input>
            </md-layout>
    
            <md-layout md-hide-large-and-up md-flex="100" v-for="field in searchableFields" :key="field.displayName">
                <h3 v-if="field.sort" @click="field.sort">
                    <md-icon v-if="field.sort">{{reverseSortOrder ? "arrow_drop_down" : "arrow_drop_up" }}</md-icon>
                    {{ field.displayName }}
                </h3>
                <h3 v-else>
                    {{ field.displayName }}
                </h3>
                <select v-if="field.type == 'select'" @change="field.search">
                    <option value=" "></option>
                    <option v-for="option in field.options " :key="option " :value="option ">{{ option }}</option>
                </select>
                <input v-else-if="field.type == 'text'" @change="field.search" type="text "></input>
            </md-layout>
        </md-layout>
    </md-layout>
</template>

<style scoped>
.header {}

h2 {
    color: #999;
}

h3 {
    cursor: pointer;
    display: inline-block;
    vertical-align: middle;
    margin: 0px 10px 0px 0px;
}

input {
    width: 150px;
    height: 25px;
    display: inline-block;
    vertical-align: middle;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";
import { Question } from "../../interfaces/models";

@Component()
export default class QuestionSearch extends Vue {
    @Prop
    availableQuestions: Question[];

    reverseSortOrder: boolean = false;
    currentFilter: string = "";

    searchableFields: Object[] = [];

    get uniqueQuestionTopics() {
        return Array.from(new Set(this.availableQuestions.map(x => x.topics).reduce((a, b) => a.concat(b))));
    }

    @Lifecycle
    created() {
        let textToSearch = "";
        let topicsToKeep = "";

        this.searchableFields = [{
            displayName: "Topic",
            search: (e: MouseEvent) => {
                if (e !== null) {
                    topicsToKeep = (e.target as HTMLFormElement).value;
                    this.applyFilters();
                }
                return x => topicsToKeep ? x.topics.find(topic => topicsToKeep == topic) !== undefined : true;
            },
            options: this.uniqueQuestionTopics,
            type: "select",
            searchValue: ""
        }, {
            displayName: "Sort",
            search: (e?: MouseEvent) => {
                if (e !== null) {
                    const itemToSortOn = (e.target as HTMLFormElement).value;
                    this.currentFilter = itemToSortOn;
                    this.applyFilters();
                }
                return x => true;
            },
            options: ["Quality", "Difficulty", "Responses"],
            type: "select",
            searchValue: ""
        }, {
            displayName: "Order",
            sort: () => {
                this.reverseSortOrder = !this.reverseSortOrder;
                this.applyFilters();
            },
            searchValue: ""
        }, {
            displayName: "Content",
            search: (e?: KeyboardEvent) => {
                if (e !== null) {
                    textToSearch = (e.target as HTMLFormElement).value;
                    this.applyFilters();
                }
                return x => x.content.toLowerCase().indexOf(textToSearch.toLowerCase()) >= 0;
            },
            searchValue: "",
            type: "text"
        }];

        this.$emit("searched", this.availableQuestions);
    }

    filter(questions) {
        const keyValue = q => {
            if (this.currentFilter == "") return 0;
            if (this.currentFilter == "Quality") return q.quality;
            if (this.currentFilter == "Difficulty") return q.difficulty;
            return q.responses.length;
        };

        if (this.reverseSortOrder) {
            return questions.sort((a, b) => keyValue(a) - keyValue(b)).reverse();
        } else {
            return questions.sort((a, b) => keyValue(a) - keyValue(b));
        };
    }

    applyFilters() {
        const searchResults = this.availableQuestions.filter(x => {
            return this.searchableFields.every((searchItem: any) => {
                if (!searchItem.search) return true;
                return searchItem.search(null)(x);
            });
        });

        this.$emit("searched", this.filter(searchResults));
    }
}
</script>
