<template>
    <md-layout md-flex="100"
               class="header">
        <md-layout v-for="field in searchableFields"
                   :key="field.displayName"
                   class="searchItem">
            <h3 v-if="field.sort"
                @click="field.sort"
                class="sortBy">{{ field.name }}
                <md-icon>{{reverseSortOrder ? "arrow_drop_down" : "arrow_drop_up" }}</md-icon>
            </h3>
            <h3 v-else>{{ field.name }}</h3>

            <select v-if="field.type == 'select'"
                    @change="field.search">
                <option v-for="option in field.options"
                        :key="option"
                        :value="option">{{ option }}</option>
            </select>

            <input v-else-if="field.type == 'text'"
                   @keyup="field.search"
                   type="text"></input>
        </md-layout>
    </md-layout>
</template>

<style scoped>
.header {
    justify-content: space-between;
    margin-bottom: 1em;
    width: 100%;
}

.searchItem {
    flex: none;
}

h2 {
    color: #999;
}

h3.sortBy {
    cursor: pointer;
}

h3 {
    user-select: none;
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
import { Vue, Component, Lifecycle, Watch, Prop, p } from "av-ts";
import { Question } from "../../interfaces/models";

@Component()
export default class QuestionSearch extends Vue {
    @Prop
    availableQuestions: Question[];

    reverseSortOrder: boolean = false;
    currentFilter: string = "";
    searchMode: string = "All Questions";

    searchableFields: Object[] = [];

    get uniqueQuestionTopics() {
        const topics = this.availableQuestions.map(x => x.topics).reduce((a, b) => a.concat(b), []);

        return Array.from(new Set(topics)).map(x => topics.find(t => t == x));
    }

    @Lifecycle
    created() {
        let textToSearch = "";

        this.searchableFields = [{
            name: "Sort By",
            search: (e?: MouseEvent) => {
                if (e !== null) {
                    const itemToSortOn = (e.target as HTMLFormElement).value;
                    this.currentFilter = itemToSortOn;
                    this.applyFilters();
                }
                return x => true;
            },
            options: ["", "Difficulty", "Personalised Rating", "Quality", "Responses", "Number Of Comments", "Time"],
            type: "select",
            sort: () => {
                this.reverseSortOrder = !this.reverseSortOrder;
                this.applyFilters();
            },
            searchValue: ""
        }, {
            name: "Show",
            search: (e?: MouseEvent) => {
                if (e !== null) {
                    this.searchMode = (e.target as HTMLFormElement).value;
                    this.applyFilters();
                }
                return x => true;
            },
            options: ["All Questions", "Unanswered Questions", "Answered Questions", "Wrongly Answered Questions"],
            type: "select",
            searchValue: ""
        }, {
            name: "Content",
            search: (e?: KeyboardEvent) => {
                if (e !== null) {
                    textToSearch = (e.target as HTMLFormElement).value.toLowerCase();
                    this.applyFilters();
                }
                return x => {
                    return x.content.toLowerCase().indexOf(textToSearch) >= 0 ||
                        x.topics.find(t => t.name.toLowerCase().indexOf(textToSearch) >= 0);
                };
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
        if (this.searchMode !== "All Questions") {
            questions = questions.filter(x => Math.random() <= 0.25);
        }

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

    @Watch("availableQuestions")
    handler() {
        this.applyFilters();
    }
}
</script>
