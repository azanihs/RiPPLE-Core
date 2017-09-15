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
        <slot></slot>
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

    timeoutId = undefined;
    searchInFlight = false;

    queue: Function[] = [];

    @Prop
    page = p<number>({
        default: 1
    });

    @Prop
    filterOut = p<string[]>({
        default: []
    });

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
            name: "Filter",
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
            name: "Search",
            id: "query",
            type: "text"
        }];
    }

    search = {
        sortField: "",
        sortDesc: false,
        filterField: "All Questions",
        query: "",
        page: 0
    }

    @Lifecycle
    created() {
        this.applyFilters();
    }

    sort() {
        this.search.sortDesc = !this.search.sortDesc;
    }

    applyFilters() {
        const search = Object.assign({}, this.search, { page: this.page, filterTopics: this.filterOut });
        QuestionService.search(search)
            .then(searchResult => {
                this.timeoutId = undefined;
                if (this.queue.length > 0) {
                    // Clear out the searches which will be ignored anyway
                    this.queue.splice(0, this.queue.length - 1);
                    this.queue.pop()();
                } else {
                    // Only bubble through the most recent search
                    this.$emit("searched", searchResult);
                }
            });
    }

    @Watch("page")
    pageChanged(newVal, oldVal) {
        this.startSearch();
    }

    @Watch("filterOut")
    topicsChanged(newVal, oldVal) {
        this.startSearch();
    }

    @Watch("search", { deep: true })
    searchWatch() {
        this.startSearch();
    }

    startSearch() {
        if (this.timeoutId === undefined) {
            this.timeoutId = setTimeout((() => this.applyFilters()), 10);
        } else {
            this.queue.push(() => {
                this.timeoutId = setTimeout((() => this.applyFilters()), 10);
            });
        }
    }

}
</script>
