import { pushNotify, mergeCache, mergeStringCache, eventBus } from "./Notify";

import { User, Badge, AcquiredBadge, UserSummary, Notification, Topic } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";

const cachedNotifications: Notification[] = [];
const cachedPeers: User[] = [];
let cachedLoggedInUser: User = undefined;
const cachedRecommendedConnections: User[] = [];

const cachedOutstandingRequests: User[] = [];

const cachedLeaderboardUsers: UserSummary[] = [];
const cachedMentoringTypes: string[] = [];
const cachedEngagementTypes: string[] = [];
const cachedMeetingHistory: { name: string }[] = [];

const queues: { [eventId: string]: Function[] } = {};

export default class UserService {
    static subscribe(event: string, callback: Function) {
        if (queues[event] === undefined) {
            queues[event] = [callback];
            eventBus.$on(event, data => {
                queues[event].forEach(cb => cb(data));
            });
        } else {
            queues[event].push(callback)
        }
    }

    static generateGraph(topicsToInclude: any[], sourceData, otherData) {

        // Only keep edges where target && source appear in topicsToInclude        
        const flattenAndFilter = topics => topics
            .reduce((a, b) => a.concat(b), [])
            .filter(x => topicsToInclude.find(topic => topic == x.source)
                && topicsToInclude.find(topic => topic == x.target));

        const ownScores = flattenAndFilter(topicsToInclude.map(sourceData));
        const userGoals = flattenAndFilter(topicsToInclude.map(otherData));

        const topics = ownScores
            .map(x => x.source)
            .reduce((carry, topicNode) => {
                if (topicsToInclude.find(x => x == topicNode) &&
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

    static userCompetencies(topicsToInclude: Topic[], compareTo: string, notify?: Function) {
        return UserService.generateGraph(topicsToInclude, UserRepository.serverAggregate("competency"), UserRepository.serverAggregate(compareTo));
    }

    static getEngagementScores(itemsToInclude: string[], compareTo: string, notify?: Function) {
        return UserService.generateGraph(itemsToInclude, UserRepository.serverAggregate("engagement"), UserRepository.serverAggregate(compareTo));
    }

    static getAllAvailableEngagementTypes(notify?: Function): string[] {
        const originalLength = cachedEngagementTypes.length;

        UserRepository.getAllAvailableEngagementTypes().then(categories => {
            categories.forEach(mergeStringCache(cachedEngagementTypes));
            if (originalLength != cachedEngagementTypes.length) {
                pushNotify(notify, cachedEngagementTypes);
            }
        });

        return cachedEngagementTypes;
    }

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
        //return UserRepository.getAllAvailableCategories();
        return [];
    }

    static getRecommendedConnections(notify?: Function, count: number) {

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

    static getOutstandingRequests(count: number): User[] {
        const originalLength = cachedOutstandingRequests.length;
        UserRepository.getUserConnections(count)
            .then(recommendations => {
                recommendations.forEach(mergeCache(cachedOutstandingRequests));
                if (originalLength !== cachedOutstandingRequests.length) {
                    eventBus.$emit("getOutstandingRequests", cachedOutstandingRequests);
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

    static getMeetingHistory(notify?: Function) {
        const originalLength = cachedMeetingHistory.length;

        UserRepository.getAllAvailableCategories().then(categories => {
            categories.forEach(mergeStringCache(cachedMeetingHistory));
            if (originalLength != cachedMeetingHistory.length) {
                pushNotify(notify, cachedMeetingHistory);
            }
        });

        return cachedMeetingHistory;
    }
}
