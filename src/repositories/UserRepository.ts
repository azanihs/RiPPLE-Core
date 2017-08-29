import { User, Badge, AcquiredBadge, Notification, Topic, PeerConnection } from "../interfaces/models";
import PeerRepository from "./PeerRepository";
import faker from "faker";

const f: any = faker;

let IDCounter = 0;
const types = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];
const getCategory: any = i => ["connections", "engagement", "competencies"][i];
const engagementTypes = ["Competencies", "Goal Progress", "Achievements", "Recommendations", "Social Connections",
    "Study Partners", "Peers Mentored", "Questions Rated", "Questions Asked", "Questions Answered", "Questions Viewed"];

const topics = new Array(10).fill(0).map(x => f.hacker.abbreviation()).filter((x, i, self) => self.indexOf(x) == i);

type NotificationType = "Incoming Connection" | "Achievement" | "Personal Goal" | "Upcoming Meeting";

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

const getRandomTopic = () => {
    const i = f.random.number({ min: 0, max: 3 });
    return ["Incoming Connection", "Achievement", "Personal Goal", "Upcoming Meeting"][i];
};
const notifications = new Array(50).fill(0).map(x => ({
    id: Math.random(),
    type: getRandomTopic() as NotificationType,
    content: f.hacker.phrase(),
    read: !!(Math.random() < 0.5)
}));

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

const makeUser = () => {
    const getType = i => {
        return types[i] as "Provide Mentorship" | "Seek Mentorship" | "Find Study Partner";
    };

    const connections = new Array(f.random.number({ min: 2, max: 10 })).fill(0).map(x => {
        const connection: PeerConnection = {
            edgeStart: 0,
            edgeEnd: 0,

            type: getType(f.random.number({ min: 0, max: 2 })),
            topic: f.random.number({ min: 0, max: 5 }),
            weight: f.random.number({ min: 0, max: 10 }),
            date: new Date(),
            availableTime: new Date()
        };
        return connection;
    });
    const proficiencies = new Array(f.random.number({ min: 1, max: 4 }))
        .fill(0).map(x => f.hacker.abbreviation()) as string[];

    const user: User = {
        id: IDCounter++,
        name: f.name.findName(),
        bio: f.hacker.phrase() + " " + f.hacker.phrase(),
        image: f.image.avatar(),

        proficiencies: proficiencies,
        connections: connections
    };
    return user;
};

const loggedInUser = makeUser();
const userPeers = new Array(100).fill(0).map(makeUser);

export default class UserRepository {

    static getLoggedInUser(): Promise<User> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(loggedInUser);
            }, Math.random() * 1000);
        });
    }

    static getUserConnections(count: number): Promise<User[]> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(userPeers.slice(0, count));
            }, Math.random() * 1000);
        });
    }

    static getUserNotifications(): Promise<Notification[]> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(notifications);
            }, Math.random() * 1000);
        });
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
