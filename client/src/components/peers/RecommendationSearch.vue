<template>
    <md-layout md-flex="100">
        <h2>Find Connections</h2>
        <md-layout md-flex="100"
                   class="componentSeparator">
            <div class="spaceBetween">
                <h2>
                  Select your roles to match with people who have complementing roles
                </h2>
                <md-switch v-model="showRoles"
                           class="md-primary switch"
                           id="roleSwitch"
                           name="roleSwitch">Show Student Roles</md-switch>
            </div>
            <table class="table">
                <thead>
                    <tr>
                        <th>Topics</th>
                        <th v-for="role in studyRoles"
                            :key="role.id">{{ role.description }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="topic in topics"
                        :key="topic.id">
                        <td>
                            <span>{{ topic.name }}</span>
                            <div class="cellOverlay"
                                 :style="getCellWeight(topic)"></div>
                        </td>
                        <td v-for="role in studyRoles"
                            :key="role.id"
                            class="centerAlign"
                            :style="getCellShade(topic, role)">
                            <md-checkbox class="centerCheckbox"
                                         :disabled="checkboxIsDisabled(role.description, topic)"
                                         :value="checkbox(topic, role)"
                                         @change="checkboxChange(topic, role)"
                                         :id="`${role.id}_${topic.id}`"
                                         :name="`${role.id}_${topic.id}`"></md-checkbox>
                        </td>
                    </tr>
                </tbody>
            </table>
        </md-layout>
        <md-layout md-flex="100">
            <h3>Suggested Connections</h3>
            <md-layout md-flex="100"
                       md-gutter="16">
                <md-layout md-flex="33"
                           md-gutter
                           class="componentSeparator"
                           v-for="(recommendation, i) in recommendations"
                           :key="i">
                    <recommendation-card :recommendation="recommendation">
                        Request
                    </recommendation-card>
                </md-layout>
            </md-layout>
        </md-layout>
    </md-layout>
</template>

<style>

    .connect-tabs .md-tabs-navigation-container {
        background-color: #4d656d;
    }

    .connect-tabs .md-tab-header {

        background-color: rgba(34,85,102, 0.7);
        border-bottom: 6px solid #f2f2f2;
    }

    .connect-tabs .md-tab-header:hover {
        background-color: rgba(34,85,102, 0.4);
    }

    .connect-tabs span {
        font-weight: bold;
        font-family: Verdana,Arial,Helvetica,sans-serif;
    }
    .connect-tabs .md-active span{
        color: #f2f2f2;
    }

    .connect-tabs .md-active {
        background-color: #256;
    }

    .connect-tabs .md-tab-indicator{
        background-color: #1d323a !important;
        height: 6px;
    }



</style>

<style scoped>
.spaceBetween {
    display: flex;
    flex: 1;
    justify-content: space-between;
}

.tab {
    padding-left: 2px !important;
    padding-right: 2px !important;
}

.table {
    border: none;
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

.table tbody td:first-child {
    position: relative;
}

.table thead tr {
    background-color: #256;
    color: #f2f2f2;
}

.table tbody tr:nth-child(even) {
    background-color: #efefef;
}

.table tr td,
.table thead tr th {
    text-align: center;
    padding: 8px 0px;
}

.cellOverlay {
    position: absolute;
    left: 0px;
    top: 5%;
    width: 0px;
    height: 90%;
    border: 1px solid transparent;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";

import { ITopic, IEdge, IStudyRole, ICompareSet, IRoleCount,
    ICourseRoleCount, ICourseRoleWeights, IRecommendation } from "../../interfaces/models";
import AvailabilityService from "../../services/AvailabilityService";
import UserService from "../../services/UserService";
import RecommendationService from "../../services/RecommendationService";
import Fetcher from "../../services/Fetcher";

import RecommendationCard from "./RecommendationCard.vue";

@Component({
    components: {
        RecommendationCard
    }
})
export default class RecommendationSearch extends Vue {
    @Prop
    topics = p<ITopic[]>({
        required: true
    });

    @Prop
    studyRoles = p<IStudyRole[]>({
        default: () => {
            return [];
        }
    });

    @Prop
    userRoles = p<Map<string, Map<string, boolean>>>({
        type: Map,
        default: () => {
            return new Map<string, Map<string, boolean>>();
        }
    });

    pShowRoles = true;
    competencies = new Map();
    pRoleWeights: ICourseRoleWeights = {};
    pFindRecommendations: IRecommendation[] = [];

    get showRoles() {
        return this.pShowRoles;
    }
    set showRoles(newVal) {
        this.pShowRoles = newVal;
    }

    get recommendations() {
        return this.pFindRecommendations;
    }

    updateCompetencies(newCompetencies: ICompareSet) {
        this.competencies = newCompetencies.ownScores
            .reduce((carry: Map<ITopic, number>, x: IEdge) => {
                if (carry.get(x.source) === undefined) {
                    carry.set(x.source, x.competency);
                }
                return carry;
            }, new Map());
    };

    updateRoleWeights(newRoleCount: ICourseRoleCount) {
        const roleCounts: [IRoleCount] = newRoleCount.counts;
        const max: number = newRoleCount.max;
        let roleWeightLookup: ICourseRoleWeights = {};
        roleCounts.map(roleCount => {
            const { topic, studyRole, entries } = roleCount;
            if (roleWeightLookup[topic] === undefined) {
                // Create the
                roleWeightLookup[topic] = { [studyRole]: entries / max };
            } else {
                roleWeightLookup[topic][studyRole] = entries / max;
            }
        });
        this.pRoleWeights = roleWeightLookup;
    };

    updateFindRecommendations(recommendations: IRecommendation[]) {
        this.pFindRecommendations = recommendations;
    };

    @Lifecycle
    created() {
        Fetcher.get(UserService.userCompetencies)
            .on(this.updateCompetencies);
        Fetcher.get(AvailabilityService.getCourseRoleCount)
            .on(this.updateRoleWeights);
        Fetcher.get(RecommendationService.findRecommendations)
            .on(this.updateFindRecommendations);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(UserService.userCompetencies)
            .off(this.updateCompetencies);
        Fetcher.get(AvailabilityService.getCourseRoleCount)
            .off(this.updateRoleWeights);
        Fetcher.get(RecommendationService.findRecommendations)
            .off(this.updateFindRecommendations);
    }

    checkbox(topic: ITopic, studyRole: IStudyRole): boolean {
        if (!this.userRoles.has(topic.name)) {
            return false;
        } else {
            const topicRoles = this.userRoles.get(topic.name);
            if (topicRoles !== undefined) {
                return topicRoles.get(studyRole.role) || false;
            }
            return false;
        }
    }

    checkboxChange(topic: ITopic, studyRole: IStudyRole) {
        this.$emit("change", topic.id, studyRole.id);
    }

    checkboxIsDisabled(sType: string, topic: ITopic) {
        if (sType == "Provide Mentorship") {
            const weight = this.competencies.get(topic);
            return weight === undefined || weight <= 85;
        }

        return false;
    }

    getColour(c: number) {
        if (c < 50) {
            return "rgba(255, 99, 132, ";
        } else if (c >= 50 && c < 85) {
            return "rgba(255, 206, 86, ";
        } else if (c >= 85) {
            return "rgba(34, 85, 102, ";
        }
    }

    getCellWeight(topic: ITopic) {
        const weight = this.competencies.get(topic);
        return {
            background: `${this.getColour(weight)}${0.4})`,
            borderColor: `${this.getColour(weight)}1)`,
            width: `${weight}%`
        };
    }

    getCellShade(topic:ITopic, studyRole:IStudyRole) {
        if (this.pShowRoles) {
            let weight = 0;
            if (this.pRoleWeights[topic.id] !== undefined) {
                if (this.pRoleWeights[topic.id][studyRole.id] !== undefined) {
                    weight = this.pRoleWeights[topic.id][studyRole.id];
                }
            }

            // Perferably have a lookup table generated on mount
            return {
                background: `rgba(34, 85, 102, ${weight})`
            };
        }
    }
}
</script>
