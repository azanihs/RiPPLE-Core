import { every, mergeCache, mergeStringCache } from "./Notify";

import { User, Badge, AcquiredBadge, UserSummary, Notification, Topic, Edge } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";
import TopicRepository from "../repositories/TopicRepository";

export default class UserService {
    static generateGraph(sourceData: Edge[], otherData: Edge[]) {
        const ownScores = sourceData;
        const userGoals = otherData;
        const topics = ownScores
            .map(x => x.source)
            .concat(ownScores.map(x => x.target))
            .reduce((carry: Topic[], topicNode: Topic) => {
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
    }

    static userCompetencies({ compareTo }: { compareTo: string }) {
        return Promise.all([UserRepository.getUserCompetencies(), UserRepository.getUserCompetencies()])
            .then(data => UserService.generateGraph(data[0], data[1]));
    }

    static getEngagementScores(itemsToInclude: string[], compareTo: string) {
        return Promise.all([UserRepository.getUserEngagement(), UserRepository.getUserEngagement()])
            .then(data => UserService.generateGraph(data[0], data[1]));
    }

    static getAllAvailableEngagementTypes() {
        return UserRepository.getAllAvailableEngagementTypes();
    }

    static getUserPeers({ connectionCount }: { connectionCount: number }) {
        return UserRepository.getUserConnections(connectionCount);
    }

    static getEngagementSummary() {
        return UserRepository.getUserEngagement()
            .then(edges => edges.filter(x => x.target == x.source)
                .map(x => ({
                    node: x.target,
                    score: x.competency
                })));
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
