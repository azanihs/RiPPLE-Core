import { User, Peer, Badge, AcquiredBadge } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";
import PeerRepository from "../repositories/PeerRepository";

export default class UserService {

    static getUserPeers() {
        return PeerRepository.getMany(20 + Math.round(Math.random() * 100))
    }

    static getEngagementBreakdown() {
        return {
            data: {
                labels: ["Browsing Peer Connections", "Viewing Questions", "Viewing Statistics Page", "Answering Questions"],
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
        }
    }

    static getComparativeEngagementBreakdown() {
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
        }
    }

    static userCompetencies() {
        const topics = UserRepository.getAllAvailableTopics();
        const ownScore = topics.map(x => Math.round(Math.random() * 100));
        const userGoal = topics.map(x => Math.round(Math.random() * 100));

        return {
            data: {
                labels: topics,
                datasets: [{
                    data: userGoal,
                    label: "Your Goal",
                    type: "line",
                    pointStyle: "triangle",
                    backgroundColor: "rgba(29, 50, 58, 1)",
                    showLine: false,
                    pointBorderColor: "rgba(29, 50, 58, 1)",
                    pointBackgroundColor: "rgba(29, 50, 58, 1)",
                }, {
                    data: ownScore,
                    label: "Your Results",
                    backgroundColor: "rgba(34, 85, 102, 0.5)",
                    borderColor: "rgba(29, 50, 58, 1)",
                    borderWidth: 1
                }]
            },
            options: {
                scale: {
                    ticks: {
                        beginAtZero: true
                    }
                },
                scales: {
                    xAxes: [{
                        stacked: true
                    }],
                    yAxes: [{
                        stacked: true
                    }]
                }
            }
        }
    }


    static getEngagementScores() {

        return ["Engagement Score", "Overall Grade", "Goal Progress", "Achievements", "Recommendations Accepted", "Social Connections", "Study Partners", "Peers Mentored", "Questions Rated", "Questions Asked", "Questions Answered", "Questions Viewed"].map(x => {
            const item = {
                name: x,
                score: Math.floor(Math.random() * 100)
            }

            return item;
        })
    }
}