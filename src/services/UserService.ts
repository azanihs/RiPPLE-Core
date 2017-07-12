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
            options: {
                scale: {
                    ticks: {
                        beginAtZero: true
                    }
                },
                animation: {
                    animateRotate: true
                }
            }
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
                    label: "Progress",
                    backgroundColor: [
                        "rgba(255, 99, 132, 0.2)"
                    ],
                    borderColor: [
                        "rgba(255,99,132,1)"
                    ]
                }, {
                    data: classAverage,
                    label: "Goal",
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
        const classAverage = topics.map(x => {
            return {
                x: x,
                y: Math.round(Math.random() * 100)
            }
        });

        return {
            data: {
                labels: topics,
                datasets: [{
                    data: classAverage,
                    label: "Your Goal",
                    type: "scatter",
                    backgroundColor: "rgba(255, 99, 132, 0.5)",
                    showLine: false,
                    pointBorderColor: "rgba(255, 99, 132, 0.5)",
                    pointBackgroundColor: "rgba(255, 99, 132, 0.5)",
                }, {
                    data: ownScore,
                    label: "Your Results",
                    backgroundColor: "#256"
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
}