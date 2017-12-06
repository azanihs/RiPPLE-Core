<template>
    <md-layout md-flex="100"
               class="header">
        <md-layout v-for="field in searchableFields"
                   :key="field.displayName"
                   class="searchItem">
            <md-input-container v-if="field.type == 'multiselect'">
                <label :for="field.name">{{field.name}}</label>
                <md-select :name="field.name" multiple v-model="search[field.id]">
                    <md-option v-for="option in field.options"
                        :key="option.value"
                        :value="option.value">{{ option.name }} </md-option>
                </md-select>
            </md-input-container>
            <md-input-container v-else-if="field.type == 'select'">
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
import { Topic } from "../../interfaces/models";

import QuestionService from "../../services/QuestionService";
import TopicService from "../../services/TopicService";
import Fetcher from "../../services/Fetcher";


interface ISearch {
    sortField: string,
    sortDesc: boolean,
    filterField: string,
    query: string,
    page: number,
    filterTopics: number[]
};

@Component()
export default class QuestionSearch extends Vue {

    timeoutId: number | undefined = undefined;
    searchInFlight = false;

    nextSearchRequest: Function| undefined = undefined;

    @Prop
    page = p<number>({
        default: 1
    });
    @Prop
    pageSize = p<number>({
        default: 25
    });

    pTopics: Topic[] = [];

    updateCourseTopics(newTopics: Topic[]) {
        this.pTopics = newTopics;
        if (this.search.filterTopics.length == 0) {
            this.search.filterTopics = newTopics.map(x => x.id);
        }
    }

    get topics() {
        return this.pTopics;
    }

    get searchableFields() {
        return [{
            name: "Sort By",
            id: "sortField",
            type: "select",
            sort: true,
            options: [{
                name: "",
                value: ""
            }, {
                name: "Difficulty",
                value: "difficultyCount"
            }, {
                name: "Quality",
                value: "qualityCount"
            }, {
                name: "Created Time",
                value: "created_time"
            }, {
                name: "Responses",
                value: "responses"
            }, {
                name: "Comments",
                value: "comments"
            }, {
                name: "Personalised Rating",
                value: "personalisation"
            }]
        }, {
            name: "Show With Topic",
            id: "filterTopics",
            type: "multiselect",
            options: this.topics.map(topic => ({
                name: topic.name,
                value: topic.id
            }))
        }, {
            name: "Filter Questions",
            id: "filterField",
            type: "select",
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
                name: "Room for Improvement",
                value: "improve"
            }]
        }, {
            name: "Search",
            id: "query",
            type: "text"
        }];
    }

    search: ISearch = {
        sortField: "",
        sortDesc: false,
        filterField: "All Questions",
        query: "",
        page: 0,
        filterTopics: []
    }

    @Lifecycle
    created() {
        this.applyFilters();
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateCourseTopics);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateCourseTopics);
    }

    sort() {
        this.search.sortDesc = !this.search.sortDesc;
    }

    applyFilters() {
        const search = Object.assign({}, this.search, { page: this.page, pageSize: this.pageSize });
        QuestionService.search(search)
            .then(searchResult => {
                this.timeoutId = undefined;
                if (this.nextSearchRequest != undefined) {
                    this.nextSearchRequest();
                    this.nextSearchRequest = undefined;
                } else {
                    // Only bubble through the most recent search
                    this.$emit("searched", searchResult);
                }
            });
    }

    @Watch("page")
    pageChanged(_newVal: number, _oldVal: number) {
        this.startSearch();
    }

    @Watch("pageSize")
    pageSizeChanged(_newVal: number, _oldVal: number) {
        this.startSearch();
    }

    @Watch("search", { deep: true })
    searchWatch(_oldValue: ISearch, _newValue: ISearch) {
        this.startSearch();
    }

    startSearch() {
        if (this.timeoutId === undefined) {
            this.timeoutId = window.setTimeout((() => this.applyFilters()), 10);
        } else {
            this.nextSearchRequest = () => {
                this.timeoutId = window.setTimeout((() => this.applyFilters()), 10);
            };
        }
    }

}
</script>
