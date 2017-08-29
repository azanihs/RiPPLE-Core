import { pushNotify, mergeCache } from "./Notify";

import { User, Peer, Badge, AcquiredBadge, UserSummary, Notification, Topic } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";
import PeerRepository from "../repositories/PeerRepository";

const cachedNotifications = [];

export default class UserService {

    static getUserPeers() {
        return PeerRepository.getMany(20 + Math.round(Math.random() * 100));
    }

    static userCompetencies(topicsToInclude: Topic[]) {
        const flattenAndFilter = topics => topics
            .reduce((a, b) => a.concat(b), [])
            .filter(x => topicsToInclude.find(topic => topic.id == x.source.id)
                && topicsToInclude.find(topic => topic.id == x.target.id));

        // Only keep edges where target && source appear in topicsToInclude
        const ownScores = flattenAndFilter(topicsToInclude.map(UserRepository.userScoreForTopic));
        const userGoals = flattenAndFilter(topicsToInclude.map(UserRepository.userGoalForTopic));

        const topics = ownScores
            .map(x => x.source)
            .reduce((carry, topicNode) => {
                if (topicsToInclude.find(x => x.id == topicNode.id) &&
                    !carry.find(x => x == topicNode)) {
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

    static getAllAvailableEngagementTypes() {
        return UserRepository.getAllAvailableEngagementTypes();
    }

    static getEngagementScores(itemsToGet: string[]) {
        // Only keep edges where target && source appear in topicsToInclude
        const flattenAndFilter = topics => topics
            .reduce((a, b) => a.concat(b), [])
            .filter(x => itemsToGet.find(topics => topics == x.source.id)
                && itemsToGet.find(topics => topics == x.target.id));

        const ownScores = flattenAndFilter(itemsToGet.map(UserRepository.userEngagementForType));
        const userGoals = flattenAndFilter(itemsToGet.map(UserRepository.engagementOtherForType));

        const topics = ownScores
            .map(x => x.source)
            .reduce((carry, topicNode) => {
                if (itemsToGet.find(x => x == topicNode.id) &&
                    !carry.find(x => x == topicNode)) {
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

    static getLoggedInUser(): User {
        return UserRepository.getLoggedInUser();
    }

    static getAllAvailableCategories(): string[] {
        return UserRepository.getAllAvailableCategories();
    }

    static getRecommendedConnections(count: number) {
        const recommendations = PeerRepository.getMany(count) as any;
        const categoryLength = this.getAllAvailableCategories().length;
        recommendations.forEach(x => {
            x.recommendationType = this.getAllAvailableCategories()[Math.floor(Math.random() * categoryLength)];
            x.availableTime = new Date(Date.now() + (Math.random() * 1000 * 60 * 60 * 24));
        });

        return recommendations;
    }

    static getOutstandingRequests(count: number) {
        const recommendations = PeerRepository.getMany(count) as any;
        const categoryLength = this.getAllAvailableCategories().length;
        recommendations.forEach(x => {
            x.recommendationType = this.getAllAvailableCategories()[Math.floor(Math.random() * categoryLength)];
            x.availableTime = new Date(Date.now() + (Math.random() * 1000 * 60 * 60 * 24));
        });

        return recommendations;
    }

    static mostReputableUsers(): UserSummary[] {
        return UserService.getOutstandingRequests(100).map(x => {
            const summary: UserSummary = {
                name: x.name,
                image: x.image,
                reputation: Math.floor(Math.random() * 20),
                questionsContributed: Math.floor(Math.random() * 20),
                numberAnswers: Math.floor(Math.random() * 20),
                numberComments: Math.floor(Math.random() * 20)
            };
            return summary;
        }).sort((a, b) => b.reputation - a.reputation);
    }

    static getUserNotifications(count: number, notify?: Function): Notification[] {
        const originalLength = cachedNotifications.length;

        UserRepository.getUserNotifications()
            .then(notifications => {
                notifications.forEach(mergeCache(cachedNotifications));
                if (originalLength !== cachedNotifications.length) {
                    pushNotify(notify, cachedNotifications);
                }
            });

        return cachedNotifications.slice(0, count);
    }

    static getMeetingHistory() {
        return ["UQ", "Toowong", "Indro", "Indooroopilly"].map(x => ({
            name: x
        }));
    }
}
