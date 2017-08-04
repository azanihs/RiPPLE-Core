import { User, Peer, Badge, AcquiredBadge } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";
import PeerRepository from "../repositories/PeerRepository";

export default class UserService {

    static getUserPeers() {
        return PeerRepository.getMany(20 + Math.round(Math.random() * 100));
    }

    static getEngagementBreakdown() {
        // TODO: only return the data in this method. The view should handle the configuration
        return {
            data: {
                labels: [
                    "Browsing Peer Connections",
                    "Viewing Questions",
                    "Viewing Statistics Page",
                    "Answering Questions"
                ],
                datasets: [{
                    data: [20, 25, 40, 50],
                    label: "Your Score",
                    backgroundColor: [
                        "rgba(255, 99, 132, 0.2)",
                        "rgba(54, 162, 235, 0.2)",
                        "rgba(255, 206, 86, 0.2)",
                        "rgba(16, 150, 21, 0.2)"
                    ],
                    borderColor: [
                        "rgba(255,99,132,1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)",
                        "rgba(16, 150, 21, 1)"
                    ]
                }]
            },
            options: {}
        };
    }

    static getComparativeEngagementBreakdown() {
        // TODO: only return the data in this method. The view should handle the configuration

        const topics = UserRepository.getAllAvailableTopics();
        const ownScore = topics.map(x => Math.round(Math.random() * 100));
        const classAverage = topics.map(x => Math.round(Math.random() * 100));
        return {
            data: {
                labels: topics,
                datasets: [{
                    data: ownScore,
                    label: "Own Score",
                    backgroundColor: [
                        "rgba(255, 99, 132, 0.2)"
                    ],
                    borderColor: [
                        "rgba(255,99,132,1)"
                    ]
                }, {
                    data: classAverage,
                    label: "Class Average",
                    backgroundColor: [
                        "rgba(54, 162, 235, 0.2)"
                    ],
                    borderColor: [
                        "rgba(54, 162, 235, 1)"
                    ]
                }]
            },
            options: {
                scale: {
                    ticks: {
                        beginAtZero: true
                    }
                }
            }
        };
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
        // TODO: only return the data in this method. The view should handle the configuration

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

    static getEngagementScores() {
        return [
            "Engagement Score",
            "Overall Grade",
            "Goal Progress",
            "Achievements",
            "Recommendations Accepted",
            "Social Connections",
            "Study Partners",
            "Peers Mentored",
            "Questions Rated",
            "Questions Asked",
            "Questions Answered",
            "Questions Viewed"].map(x => {
                const item = {
                    name: x,
                    score: Math.floor(Math.random() * 100)
                };

                return item;
            });
    }


    /**
 * Returns an array of Peer objects
 * @param {number} peerCount The number of peers to return
 * @return {Peer[]} An array of Peers with length peerCount
 */
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
}
