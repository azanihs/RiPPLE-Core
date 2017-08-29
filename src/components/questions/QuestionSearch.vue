<template>
    <md-layout md-flex="100"
               class="header">
        <md-layout v-for="field in searchableFields"
                   :key="field.displayName"
                   class="searchItem">
            <h3 v-if="field.sort"
                @click="sort"
                class="sortBy">{{ field.name }}
                <md-icon>{{search.sortDesc ? "arrow_drop_down" : "arrow_drop_up" }}</md-icon>
            </h3>
            <h3 v-else>{{ field.name }}</h3>

            <select v-if="field.type == 'select'"
                    v-model="search[field.id]"
                    @change="field.search">
                <option v-for="option in field.options"
                        :key="option.value"
                        :value="option.value">{{ option.name }}</option>
            </select>

            <input v-else-if="field.type == 'text'"
                   v-model="search[field.id]"
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
import QuestionService from "../../services/QuestionService";

@Component()
export default class QuestionSearch extends Vue {
    @Prop
    availableQuestions: Question[];

    timeoutId = undefined;
    searchInFlight = false;

    get uniqueQuestionTopics() {
        const topics = this.availableQuestions.map(x => x.topics).reduce((a, b) => a.concat(b), []);
        return Array.from(new Set(topics)).map(x => topics.find(t => t == x));
    }

    get searchableFields() {
        return [{
            name: "Sort By",
            id: "sortField",
            sort: true,
            options: [{
                name: "",
                value: ""
            }, {
                name: "Difficulty",
                value: "difficulty"
            }, {
                name: "Quality",
                value: "quality"
            }, {
                name: "Created Time",
                value: "created"
            }, {
                name: "Responses",
                value: "responses"
            }, {
                name: "Comments",
                value: "comments"
            }, {
                name: "Personalised Rating",
                value: "personalisation"
            }],
            type: "select"
        }, {
            name: "Show",
            id: "filterField",
            options: [{
                name: "All Questions",
                value: ""
            }, {
                name: "Unanswered Questions",
                value: "unanswered"
            }, {
                name: "Answered Questions",
                value: "answered"
            }, {
                name: "Incorrectly Answered",
                value: "wrong"
            }],
            type: "select"
        }, {
            name: "Content",
            id: "query",
            type: "text"
        }];
    }

    search = {
        sortField: "",
        sortDesc: false,
        filterField: "All Questions",
        query: ""
    }

    @Lifecycle
    created() {
        this.$emit("searched", this.availableQuestions);
    }

    sort() {
        this.search.sortDesc = !this.search.sortDesc;
    }

    applyFilters() {
        this.searchInFlight = true;
        QuestionService.search(this.search, result => {
            this.searchInFlight = false;
            this.$emit("searched", result);
        });
    }

    @Watch("search", { deep: true })
    searchWatch() {
        if (this.searchInFlight !== false) {
            return;
        } else if (this.timeoutId !== undefined) {
            clearTimeout(this.timeoutId);
        }
        this.timeoutId = setTimeout(this.applyFilters, 250);
    }

    @Watch("availableQuestions")
    handler() {
        this.applyFilters();
    }
}
</script>
