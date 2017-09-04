import { every, mergeCache, mergeStringCache } from "./Notify";

import { User, Badge, AcquiredBadge, UserSummary, Notification, Topic } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";
import TopicRepository from "../repositories/TopicRepository";
// import CacheService from "./CacheService";

export default class UserService {
    static generateGraph(sourceData, otherData) {
        return Promise.all([sourceData, otherData])
            .then(data => {
                const sourceData = data[0].map(TopicRepository.topicPointer);
                const otherData = data[1].map(TopicRepository.topicPointer);

                // Only keep edges where target && source appear in topicsToInclude
                /*const flattenAndFilter = topics => topics
                    .reduce((a, b) => a.concat(b), [])
                    .filter(x => topicsToInclude.find(topic => topic == x.source)
                        && topicsToInclude.find(topic => topic == x.target));*/

                //const ownScores = flattenAndFilter(topicsToInclude.map(sourceData));
                //const userGoals = flattenAndFilter(topicsToInclude.map(otherData));
                const ownScores = sourceData;
                const userGoals = otherData;

                const topics = ownScores
                    .map(x => x.source)
                    .reduce((carry, topicNode) => {
                        if (!carry.find(x => x == topicNode)) {
                            carry.push(topicNode);
                        }
                        return carry;
                    }, []);
                return {
                    topics: topics, // Node List
                    ownScores: ownScores, // Edge list of self
                    compareAgainst: userGoals // Edge list of other
                };
            });
    }

    static userCompetencies({ compareTo }: { compareTo: string }) {
        return UserService.generateGraph(
            UserRepository.getUserCompetencies(),
            UserRepository.getUserCompetencies());
    }

    static getEngagementScores(itemsToInclude: string[], compareTo: string) {
        // return UserService.generateGraph(itemsToInclude, UserRepository.serverAggregate("engagement"), UserRepository.serverAggregate(compareTo));
    }

    static getAllAvailableEngagementTypes() {
        return UserRepository.getAllAvailableEngagementTypes();
    }

    static getUserPeers({ connectionCount }: { connectionCount: number }) {
        return UserRepository.getUserConnections(connectionCount);
    }

    static getLoggedInUser() {
        return UserRepository.getLoggedInUser();
    }

    static getAllAvailableCategories() {
        return UserRepository.getAllAvailableCategories();
    }

    static getRecommendedConnections({ count }: { count: number }) {
        return UserRepository.getUserConnections(count);
    }

    static getOutstandingRequests({ count }: { count: number }) {
        return UserRepository.getUserConnections(count);
    }

    static mostReputableUsers() {
        return UserRepository.getUserConnections(100)
            .then(leaders => leaders.map(x => {
                const summary: UserSummary = {
                    name: x.name,
                    image: x.image,
                    reputation: Math.floor(Math.random() * 20),
                    questionsContributed: Math.floor(Math.random() * 20),
                    numberAnswers: Math.floor(Math.random() * 20),
                    numberComments: Math.floor(Math.random() * 20)
                };
                return summary;
            }))
            .then(leaders => leaders.sort((a, b) => b.reputation - a.reputation));
    }

    static getUserNotifications() {
        return UserRepository.getUserNotifications();
    }

    static getMeetingHistory() {
        return UserRepository.getMeetingHistory();
    }
}
