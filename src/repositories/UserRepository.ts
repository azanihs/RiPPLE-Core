
import { User, Badge, AcquiredBadge, Notification, Topic, PeerConnection, Edge } from "../interfaces/models";
import TopicRepository from "./TopicRepository";
import { setToken, apiFetch } from "./APIRepository";

import faker from "faker";

const f: any = faker;

let IDCounter = 0;
const types = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];
const getCategory: any = i => ["connections", "engagement", "competencies"][i];
const engagementTypes = ["Competencies", "Goal Progress", "Achievements", "Recommendations", "Social Connections",
    "Study Partners", "Peers Mentored", "Questions Rated", "Questions Asked", "Questions Answered", "Questions Viewed"];

const topics = Array.from({ length: 10 }, x => f.hacker.abbreviation()).filter((x, i, self) => self.indexOf(x) == i);

type NotificationType = "Incoming Connection" | "Achievement" | "Personal Goal" | "Upcoming Meeting";

const userTopicScores = {};
const topicNodes = topics.map((x, id) => {
    const topicNode = {
        id: id,
        name: x
    };
    // Ensure at least one self-loop per topic
    userTopicScores[id] = [[topicNode, topicNode, Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]];
    return topicNode;
});
topicNodes.forEach(x => {
    const randomNode = topicNodes[Math.floor(Math.random() * topicNodes.length)];
    if (randomNode == x) {
        return;
    }
    userTopicScores[x.id].push([x, randomNode, Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]);
});

const getRandomTopic = () => {
    const i = f.random.number({ min: 0, max: 3 });
    return ["Incoming Connection", "Achievement", "Personal Goal", "Upcoming Meeting"][i];
};
const notifications = Array.from({ length: 50 }).map(x => ({
    id: Math.random(),
    type: getRandomTopic() as NotificationType,
    content: f.hacker.phrase(),
    read: !!(Math.random() < 0.5)
}));

const engagementNodes = engagementTypes.map(x => ({
    id: x,
    name: x
}));

const userEngagementScores = [];
engagementNodes.forEach(engagementNode => {
    // Ensure at least one self-loop per topic
    userEngagementScores.push([engagementNode, engagementNode,
        Math.floor(Math.random() * 100), Math.floor(Math.random() * 100)]);

    const randomNode = engagementNodes[Math.floor(Math.random() * engagementNodes.length)];
    if (randomNode == engagementNode) {
        return;
    }

    userEngagementScores.push([engagementNode, randomNode,
        Math.floor(Math.random() * 100),
        Math.floor(Math.random() * 100)]);
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
            topic: f.random.number({ min: 1, max: 6 }),
            weight: f.random.number({ min: 0, max: 10 }),
            date: new Date(),
            availableTime: new Date()
        };
        return connection;
    });
    const proficiencies = Array.from({ length: f.random.number({ min: 1, max: 4 }) },
        x => f.hacker.abbreviation()) as string[];

    const user: User = {
        id: IDCounter++,
        name: f.name.findName(),
        bio: f.hacker.phrase() + " " + f.hacker.phrase(),
        image: f.image.avatar(),

        availableTime: new Date(),
        proficiencies: proficiencies,
        connections: connections
    };
    return user;
};

const loggedInUser = makeUser();

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
                resolve(Array.from({ length: count }, makeUser));
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

    static getAllAvailableCategories(): Promise<string[]> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(types.slice());
            }, Math.random() * 1000);
        });
    }

    static getAllAvailableEngagementTypes(): Promise<{ id: string, name: string }[]> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(engagementNodes);
            }, Math.random() * 1000);
        });
    }

    static getUserCompetencies(): Promise<Edge[]> {
        return apiFetch(`/questions/competencies/all/`)
            .then(x => x.json())
            .then(x => x.map(x => {
                const edge: Edge = {
                    source: TopicRepository.topicPointer(x[0]),
                    target: TopicRepository.topicPointer(x[1]),
                    competency: x[2],
                    attempts: x[3]
                };
                return edge;
            }));
    }

    static getUserEngagement(): Promise<Edge[]> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(userEngagementScores.map(x => {
                    const edge: Edge = {
                        source: x[0] as Topic,
                        target: x[1] as Topic,
                        competency: x[2],
                        attempts: x[3]
                    };
                    return edge;
                }));
            }, Math.random() * 1000);
        });
    }

    static getMeetingHistory(): Promise<string[]> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(["Toowong", "UQ", "University Of Queensland", "Kenmore", "Indro"]);
            }, Math.random() * 1000);
        });
    }

    static authenticate(): Promise<void> {
        return apiFetch(`/users/login/`)
            .then(x => x.json())
            .then(x => {
                setToken(x.token);
            });
    }
}
