import { User, Peer, Badge, AcquiredBadge, Notification } from "../interfaces/models";
import PeerRepository from "./PeerRepository";
import faker from "faker";

const f: any = faker;

let IDCounter = 0;
const types = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];
const getCategory: any = i => ["connections", "engagement", "competencies"][i];

const topics = new Array(10).fill(0).map(x => f.hacker.abbreviation()).filter((x, i, self) => self.indexOf(x) == i);
const badges = new Array(30).fill(0).map((x, i) => {
    return ({
        id: i,
        category: getCategory(f.random.number({ min: 0, max: 2 })),
        name: f.company.bsBuzz(),
        description: f.company.catchPhrase()
    });
});

const userTopicScores = {};
const userGoalScores = {};

const topicNodes = topics.map(x => {
    const topicNode = {
        id: x
    };
    userTopicScores[x] = [topicNode, topicNode, Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)];
    userGoalScores[x] = [topicNode, topicNode, Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)];
    return topicNode;
});

topicNodes.forEach(x => {
    const randomNode = topicNodes[Math.floor(Math.random() * topicNodes.length)];
    if (randomNode == x) {
        return;
    }
    userTopicScores[x.id].push([x, randomNode, Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]);
});
topicNodes.forEach(x => {
    const randomNode = topicNodes[Math.floor(Math.random() * topicNodes.length)];
    if (randomNode == x) {
        return;
    }
    userGoalScores[x.id].push([x, randomNode, Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]);
});

const userBadges = badges
    .filter((_, i) => Math.random() < 0.5)
    .map((x: Badge) => {
        const acquiredBadge: AcquiredBadge = {
            badge: x,
            progress: Math.random() < 0.5 ? (Math.random() * 100) : -1,
            dateAcquired: new Date()
        };
        return acquiredBadge;
    });

export default class UserRepository {

    /**
     * Returns an array of Peer objects
     * @param {number} peerCount The number of peers to return
     * @return {Peer[]} An array of Peers with length peerCount
     */
    static getLoggedInUser(): User {
        const peer: Peer = PeerRepository.getMany(1)[0];
        const connections = new Array(f.random.number({ min: 2, max: 10 })).fill(0).map(x => {
            const connection = {
                id: IDCounter++,
                type: types[f.random.number({ min: 0, max: 2 })],
                topic: topics[f.random.number({ min: 0, max: 10 })],
                weight: f.random.number({ min: 0, max: 10 })
            };
            return connection;
        });

        const user: User = {
            id: IDCounter++,
            self: peer,
            connections: connections
        };

        return user;
    }

    static getUserNotifications(): Notification[] {
        const getRandomTopic = () => {
            const i = f.random.number({ min: 0, max: 3 });
            return ["Incoming Connection", "Achievement", "Personal Goal", "Upcoming Meeting"][i];
        };

        return new Array(50).fill(0).map(x => ({
            id: Math.random(),
            type: getRandomTopic() as "Incoming Connection" | "Achievement" | "Personal Goal" | "Upcoming Meeting",
            content: f.hacker.phrase(),
            read: !!(Math.random() < 0.5)
        }));
    }

    static getAllAvailableBadges(): Badge[] {
        return badges.slice();
    }
    static getAllUserBadges(): AcquiredBadge[] {
        return userBadges.slice();
    }

    static getAllAvailableCategories(): string[] {
        return types.slice();
    }
    static getAllAvailableTopics(): string[] {
        return topics.slice();
    }

    static userScoreForTopic(topic: string) {
        return {
            source: userTopicScores[topic][0],
            target: userTopicScores[topic][1],
            competency: userTopicScores[topic][2],
            attempts: userTopicScores[topic][3]
        };
    }

    static userGoalForTopic(topic: string) {
        return {
            source: userGoalScores[topic][0],
            target: userGoalScores[topic][1],
            competency: userGoalScores[topic][2],
            attempts: userGoalScores[topic][3]
        };
    }

}
