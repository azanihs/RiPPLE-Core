<template>
    <md-layout md-flex="100"
               class="header">
        <md-layout v-for="field in searchableFields"
                   :key="field.displayName"
                   class="searchItem">
            <md-input-container v-if="field.type == 'select'">
                <label :for="field.name">{{field.name}}</label>
                <md-select :name="field.name"
                           :id="field.name"
                           v-model="search[field.id]">
                    <md-option v-for="option in field.options"
                               :key="option.value"
                               :value="option.value">{{ option.name }}</md-option>
                </md-select>
                <h3 v-if="field.sort && search[field.id] != ''"
                    @click="sort"
                    class="sortBy">{{ search.sortDesc ? "Descending" : "Ascending"}}
                    <md-icon :class="{rotate: search.sortDesc}">arrow_upward</md-icon>
                </h3>
            </md-input-container>

            <md-input-container v-else-if="field.type == 'text'">
                <label>{{field.name}}</label>
                <md-input class="searchField"
                          v-model="search[field.id]"></md-input>
            </md-input-container>
        </md-layout>
    </md-layout>
</template>

<style scoped>
.rotate {
    transform: rotate(-180deg);
}

.header {
    justify-content: space-between;
    width: 100%;
}

.searchItem {
    flex: none;
}

h2 {
    color: #999;
}

.sortBy {
    cursor: pointer;
    display: inline-flex;
    margin-left: 25px;
    align-items: center;
    color: rgba(0, 0, 0, 0.54);
    font-size: 16px;
    font-weight: 400;
}

.sortBy>i {
    font-size: 16px;
    padding-left: 6px;
    cursor: pointer;
    transition: 250ms ease transform;
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

.searchField {
    font-size: 16px !important;
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
        QuestionService.search(this.search)
            .then(searchResult => {
                this.$emit("searched", searchResult);
            });
    }

    @Watch("search", { deep: true })
    searchWatch() {
        if (this.timeoutId !== undefined) {
            clearTimeout(this.timeoutId);
        }

        this.timeoutId = setTimeout((() => this.applyFilters()), 250);
    }

    @Watch("availableQuestions")
    handler() {
        this.applyFilters();
    }
}
</script>
