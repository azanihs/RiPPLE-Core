import { User, Peer, Badge, AcquiredBadge, UserSummary, Notification } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";
import PeerRepository from "../repositories/PeerRepository";

export default class UserService {

    static getUserPeers() {
        return PeerRepository.getMany(20 + Math.round(Math.random() * 100));
    }

    static userCompetencies(topicsToInclude: string[]) {
        const ownScore = topicsToInclude.map(x => Math.round(Math.random() * 100));
        const userGoal = topicsToInclude.map(x => Math.round(Math.random() * 100));

        const average = Math.round(ownScore.reduce((a, b) => a + b, 0) / ownScore.length);
        const goal = Math.round(Math.random() * 100);

        return {
            topics: ["Overall"].concat(topicsToInclude),
            ownScore: [average].concat(ownScore),
            compareAgainst: [goal].concat(userGoal)
        };
    }

    static userCompetenciesOverview() {
        const topics = UserRepository.getAllAvailableTopics();
        const ownScore = topics.map(x => Math.round(Math.random() * 100));
        const userGoal = topics.map(x => Math.round(Math.random() * 100));

        return {
            data: {
                labels: topics,
                datasets: [{
                    data: ownScore,
                    label: "Your Qualification",
                    borderWidth: 1,
                    backgroundColor: [],
                    borderColor: []
                }]
            },
            options: {}
        };
    }

    static getEngagementScores(itemsToGet: string[]) {
        const ownScore = itemsToGet.map(x => Math.round(Math.random() * 100));
        const userGoal = itemsToGet.map(x => Math.round(Math.random() * 100));

        const average = Math.round(ownScore.reduce((a, b) => a + b, 0) / ownScore.length);
        const goal = Math.round(Math.random() * 100);

        return {
            topics: ["Overall"].concat(itemsToGet),
            ownScore: [average].concat(ownScore),
            compareAgainst: [goal].concat(userGoal)
        };
    }

    static getLoggedInUser(): User {
        return UserRepository.getLoggedInUser();
    }

    static getAllAvailableBadges(): Badge[] {
        return UserRepository.getAllAvailableBadges();
    }

    static getAllUserBadges(): AcquiredBadge[] {
        return UserRepository.getAllUserBadges();
    }

    static getAllAvailableCategories(): string[] {
        return UserRepository.getAllAvailableCategories();
    }

    static getRecommendedConnections(count: number) {
        return PeerRepository.getMany(count);
    }

    static getOutstandingRequests(count: number) {
        return PeerRepository.getMany(count);
    }

    static userHasBadge(badgeId) {
        // TODO: This lookup is slow, a hashmap or similar would be better.
        return UserRepository.getAllUserBadges().find(x => x.badge.id == badgeId);
    }

    static mostReputableUsers(): UserSummary[] {
        return UserService.getOutstandingRequests(10).map(x => {
            const summary: UserSummary = {
                name: x.name,
                reputation: Math.floor(Math.random() * 20),
                questionsContributed: Math.floor(Math.random() * 20),
                numberAnswers: Math.floor(Math.random() * 20),
                numberComments: Math.floor(Math.random() * 20)
            };
            return summary;
        }).sort((a, b) => b.reputation - a.reputation);
    }

    static getUserNotifications(count: number): Notification[] {
        return UserRepository.getUserNotifications().slice(0, count);
    }
}
