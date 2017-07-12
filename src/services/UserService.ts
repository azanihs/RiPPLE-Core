import { User, Peer, Badge, AcquiredBadge } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";
import f from "faker";


export default class UserService {
    static getEngagementBreakdown() {
        return {
            data: {
                labels: ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"],
                datasets: [{
                    data: [20, 10, 40],
                    label: "Your Score",
                    backgroundColor: [
                        "rgba(255, 99, 132, 0.2)",
                        "rgba(54, 162, 235, 0.2)",
                        "rgba(255, 206, 86, 0.2)"
                    ],
                    borderColor: [
                        "rgba(255,99,132,1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)"
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
                    label: "Your Results",
                    backgroundColor: [
                        "rgba(255, 99, 132, 0.2)"
                    ],
                    borderColor: [
                        "rgba(255,99,132,1)"
                    ]
                }, {
                    data: classAverage,
                    label: "Class  Average",
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
}