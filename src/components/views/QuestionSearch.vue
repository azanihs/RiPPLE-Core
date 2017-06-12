<template>
    <md-layout md-flex="100">
        <h2>Search </h2>
        <md-layout md-flex="100" class="header">
            <md-layout v-for="field in searchableFields" :key="field.displayName">
                <h3 @click="sortOrder(field, $event)">
                    <md-icon>{{field.reverse ? "arrow_drop_down" : "arrow_drop_up" }}</md-icon>
                    {{ field.displayName }}
                </h3>
                <input @change="search(field, $event)" type="text" />
            </md-layout>
        </md-layout>
    </md-layout>
</template>

<style scoped>
    .header {
        margin: 15px 0px;
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
        searchableFields: Object[] = [];

        @Lifecycle
        created() {
            const numberSort = (a, b) => a - b;
            const stringSort = (a, b) => a.localeCompare(b);

            const sort = field => sorter => toSort =>
                toSort.sort((a, b) => sorter(a[field], b[field]));

            const search = field => val => this.availableQuestions
                .filter(x => `${x[field]}`.toLowerCase()
                    .indexOf(`${val}`.toLowerCase()) >= 0);

            this.searchableFields = [{
                displayName: "Quality",
                sort: sort("quality")(numberSort),
                search: search("quality"),
                reverse: false,
                searchValue: ""
            }, {
                displayName: "Difficulty",
                sort: sort("difficulty")(numberSort),
                search: search("difficulty"),
                reverse: false,
                searchValue: ""
            }, {
                displayName: "Topic",
                sort: sort("topic")(stringSort),
                search: search("topic"),
                reverse: false,
                searchValue: ""
            }, {
                displayName: "Content",
                sort: sort("content")(stringSort),
                search: search("content"),
                reverse: false,
                searchValue: ""
            }, {
                displayName: "Responses",
                sort: sort("responseCount")(numberSort),
                search: search("responseCount"),
                reverse: false,
                searchValue: ""
            }];

            this.$emit("searched", this.availableQuestions);
        }


        sortOrder(field, event: MouseEvent) {
            const originalField = field.reverse;
            this.searchableFields.forEach((field: any) => {
                field.reverse = false;
            });
            field.reverse = !originalField;
            this.reverseSortOrder = !originalField;

            this.search(field, null);
        }

        search(searchField: any, event: KeyboardEvent) {
            if (searchField && event) {
                searchField.searchValue = (event.target as HTMLInputElement).value;
            }

            let appliedSearches = [];
            let numberSearches = 0;
            this.searchableFields.forEach((field: any) => {
                if (field.searchValue) {
                    numberSearches++;
                    appliedSearches = appliedSearches.concat(
                        field.search(field.searchValue)
                    );
                }
            });

            let sortedQuestions = [];
            if (numberSearches == 0) {
                sortedQuestions = this.availableQuestions;
            } else {
                sortedQuestions = this.availableQuestions
                    .reduce((searchResults: Question[], question: Question) => {
                        const matches = appliedSearches
                            .filter((x: Question) => x.id == question.id);
                        if (matches.length == numberSearches) {
                            searchResults.push(question);
                        }
                        return searchResults;
                    }, []);
            }

            sortedQuestions = searchField.sort(sortedQuestions);
            if (this.reverseSortOrder) {
                sortedQuestions.reverse();
            }

            return this.$emit("searched", sortedQuestions);
        }
    }
</script>
