import { pushNotify, mergeCache } from "./Notify";

import { User, Badge, AcquiredBadge, UserSummary, Notification, Topic } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";

const cachedNotifications = [];
const cachedPeers = [];
let cachedLoggedInUser = undefined;
const cachedRecommendedConnections = [];
const cachedOutstandingRequests = [];

const cachedLeaderboardUsers = [];

export default class UserService {

    static getUserPeers(notify?: Function) {
        const originalLength = cachedPeers.length;
        UserRepository.getUserConnections(20 + Math.round(Math.random() * 100))
            .then(peers => {
                peers.forEach(mergeCache(cachedPeers));
                if (originalLength !== cachedPeers.length) {
                    pushNotify(notify, cachedPeers);
                }
            });

        return cachedPeers;
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

    static getLoggedInUser(notify?: Function): User {
        const originalID = cachedLoggedInUser === undefined ? -1 : cachedLoggedInUser.id;
        UserRepository.getLoggedInUser().then(user => {
            if (originalID !== user.id) {
                cachedLoggedInUser = user;
                pushNotify(notify, cachedLoggedInUser);
            }
        });

        return cachedLoggedInUser;
    }

    static getAllAvailableCategories(): string[] {
        return UserRepository.getAllAvailableCategories();
    }

    static getRecommendedConnections(count: number, notify?: Function) {
        const originalLength = cachedRecommendedConnections.length;
        UserRepository.getUserConnections(count)
            .then(recommendations => {
                recommendations.forEach(mergeCache(cachedRecommendedConnections));
                if (originalLength !== cachedRecommendedConnections.length) {
                    pushNotify(notify, cachedRecommendedConnections);
                }
            });
        return cachedRecommendedConnections;
    }

    static getOutstandingRequests(count: number, notify?: Function) {
        const originalLength = cachedOutstandingRequests.length;
        UserRepository.getUserConnections(count)
            .then(recommendations => {
                recommendations.forEach(mergeCache(cachedOutstandingRequests));
                if (originalLength !== cachedOutstandingRequests.length) {
                    pushNotify(notify, cachedOutstandingRequests);
                }
            });
        return cachedOutstandingRequests;
    }

    static mostReputableUsers(notify?: Function): UserSummary[] {
        const originalLength = cachedLeaderboardUsers.length;
        UserRepository.getUserConnections(100)
            .then(leaders => {
                leaders.map(x => {
                    const summary: UserSummary = {
                        name: x.name,
                        image: x.image,
                        reputation: Math.floor(Math.random() * 20),
                        questionsContributed: Math.floor(Math.random() * 20),
                        numberAnswers: Math.floor(Math.random() * 20),
                        numberComments: Math.floor(Math.random() * 20)
                    };
                    return summary;
                })
                    .sort((a, b) => b.reputation - a.reputation)
                    .forEach(mergeCache(cachedLeaderboardUsers));

                if (originalLength !== cachedLeaderboardUsers.length) {
                    pushNotify(notify, cachedLeaderboardUsers);
                }
            });
        return cachedLeaderboardUsers;
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
