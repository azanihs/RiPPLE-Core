import { User, Peer, Badge, AcquiredBadge, Notification, Topic } from "../interfaces/models";
import PeerRepository from "./PeerRepository";
import faker from "faker";

const f: any = faker;

let IDCounter = 0;
const types = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];
const getCategory: any = i => ["connections", "engagement", "competencies"][i];
const engagementTypes = ["Competencies", "Goal Progress", "Achievements", "Recommendations", "Social Connections",
    "Study Partners", "Peers Mentored", "Questions Rated", "Questions Asked", "Questions Answered", "Questions Viewed"];

const topics = new Array(10).fill(0).map(x => f.hacker.abbreviation()).filter((x, i, self) => self.indexOf(x) == i);


const userTopicScores = {};
const userGoalScores = {};
const topicNodes = topics.map((x, id) => {
    const topicNode = {
        id: id,
        name: x
    };
    // Ensure at least one self-loop per topic
    userTopicScores[id] = [[topicNode, topicNode, Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]];
    userGoalScores[id] = [[topicNode, topicNode, Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]];
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

const userEngagementScores = {};
const otherEngagementScores = {};
const engagementNodes = engagementTypes.map(x => {
    const engagementNode = {
        id: x
    };
    // Ensure at least one self-loop per topic
    userEngagementScores[x] = [[engagementNode, engagementNode,
        Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]];
    otherEngagementScores[x] = [[engagementNode, engagementNode,
        Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]];
    return engagementNode;
});
engagementNodes.forEach(x => {
    const randomNode = engagementNodes[Math.floor(Math.random() * engagementNodes.length)];
    if (randomNode == x) {
        return;
    }
    userEngagementScores[x.id].push([x, randomNode, Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]);
});
engagementNodes.forEach(x => {
    const randomNode = engagementNodes[Math.floor(Math.random() * engagementNodes.length)];
    if (randomNode == x) {
        return;
    }
    otherEngagementScores[x.id].push([x, randomNode, Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]);
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

    static getAllAvailableCategories(): string[] {
        return types.slice();
    }

    static getAllAvailableEngagementTypes(): string[] {
        return engagementTypes.slice();
    }

    static userEngagementForType(type: string) {
        return userEngagementScores[type].map(x => ({
            source: x[0],
            target: x[1],
            competency: x[2],
            attempts: x[3]
        }));
    }

    static engagementOtherForType(type: string) {
        return otherEngagementScores[type].map(x => ({
            source: x[0],
            target: x[1],
            competency: x[2],
            attempts: x[3]
        }));
    }

    static userScoreForTopic(topic: Topic) {
        return userTopicScores[topic.id].map(x => ({
            source: x[0],
            target: x[1],
            competency: x[2],
            attempts: x[3]
        }));
    }

    static userGoalForTopic(topic: Topic) {
        return userGoalScores[topic.id].map(x => ({
            source: x[0],
            target: x[1],
            competency: x[2],
            attempts: x[3]
        }));
    }

}
