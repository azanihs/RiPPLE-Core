import {
    CourseUser, User, Course, Badge, AcquiredBadge,
    Notification, Topic, PeerConnection, Edge, UserSummary
} from "../interfaces/models";
import TopicRepository from "./TopicRepository";
import { setToken, apiFetch } from "./APIRepository";

let IDCounter = 0;
const types = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];
const getCategory: any = i => ["connections", "engagement", "competencies"][i];
const engagementTypes = ["Competencies", "Goal Progress", "Achievements", "Recommendations", "Social Connections",
    "Study Partners", "Peers Mentored", "Questions Rated", "Questions Asked", "Questions Answered", "Questions Viewed"];

const _topics = ["Arrays", "Loops", "Recursion", "Algorithms", "Data Structures", "Variables"];

type NotificationType = "Incoming Connection" | "Achievement" | "Personal Goal" | "Upcoming Meeting";

const _n = i => Math.floor(Math.random() * i);

const userTopicScores = {};
const topicNodes = _topics.map((x, id) => {
    const topicNode = {
        id: id,
        name: x
    };
    // Ensure at least one self-loop per topic
    userTopicScores[id] = [[topicNode, topicNode, _n(100), _n(100)]];
    return topicNode;
});
topicNodes.forEach(x => {
    const randomNode = topicNodes[_n(topicNodes.length)];
    if (randomNode == x) {
        return;
    }
    userTopicScores[x.id].push([x, randomNode, _n(100), _n(100)]);
});

const _notificationMessages = [
    "Upcoming meeting",
    "New achievement unlocked!",
    "New peer recommendation",
    "Personal goal met",
    "Personal goals slipping",
    "User meeting requested",
    "User meeting accepted",
    "New achievements made available",
    "Achievement lost"
];

const getRandomTopic = () => {
    const i = _n(4);
    return ["Incoming Connection", "Achievement", "Personal Goal", "Upcoming Meeting"][i];
};

const notificationCount = Math.random() < 0.5 ? 50 : 0;
const notifications = Array.from({ length: notificationCount }).map(x => ({
    id: Math.random(),
    type: getRandomTopic() as NotificationType,
    content: _notificationMessages[_n(_notificationMessages.length)],
    read: Math.random() < 0.5
}));

const engagementNodes = engagementTypes.map(x => ({
    id: x,
    name: x
}));

const userEngagementScores = [];
engagementNodes.forEach(engagementNode => {
    // Ensure at least one self-loop per topic
    userEngagementScores.push([engagementNode, engagementNode,
        _n(100), _n(100)]);

    const randomNode = engagementNodes[_n(engagementNodes.length)];
    if (randomNode == engagementNode) {
        return;
    }

    userEngagementScores.push([engagementNode, randomNode,
        _n(100),
        _n(100)]);
});

const makeUser = () => {
    const getType = i => {
        return types[i] as "Provide Mentorship" | "Seek Mentorship" | "Find Study Partner";
    };

    const connections = new Array(2 + _n(8)).fill(0).map(x => {
        const connection: PeerConnection = {
            edgeStart: 0,
            edgeEnd: 0,
            type: getType(_n(2)),
            topic: _topics[_n(6)],
            weight: _n(10),
            date: new Date(),
            availableTime: new Date()
        };
        return connection;
    });
    const proficienciesLength = 1 + _n(3);
    const proficiencies = Array.from({ length: proficienciesLength },
        x => _topics[_n(_topics.length)]) as string[];

    const user: User = {
        id: IDCounter++,
        name: "_",
        bio: "_",
        image: "//loremflickr.com/320/240/person",

        availableTime: new Date(),
        proficiencies: proficiencies,
        connections: connections
    };
    return user;
};

const userConnections = makeUser().connections;
let _courseCode = "";

export default class UserRepository {
    static getLoggedInUser(): Promise<CourseUser> {
        return apiFetch(`/users/me/`)
            .then(x => x.json());
    }

    static getUserCourses(): Promise<Course[]> {
        return apiFetch(`/users/courses/`)
            .then(x => x.json());
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

    static getUserLeaderboard(sortField: string, sortOrder: "DESC" | "ASC"): Promise<UserSummary[]> {
        return apiFetch(`/questions/leaderboard/${sortField}/${sortOrder}/`)
            .then(x => x.json());
    }

    static getCompareAgainst(compareTo: string): Promise<Edge[]> {
        return apiFetch(`/questions/competencies/aggregate/${compareTo}`)
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

    static getMeetingHistory(): Promise<{name: string, id: number }[]> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(["Toowong", "UQ", "University Of Queensland",
                    "Kenmore", "Indro"].map((x, i) => ({ name: x, id: i })));
            }, Math.random() * 1000);
        });
    }

    static getCurrentCourse(courseCode: string) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(courseCode);
            }, Math.random() * 1000);
        });
    }

    static setCurrentCourse(courseCode: string) {
        _courseCode = courseCode;
    }

    static setCurrentToken(token: string) {
        setToken(token);
    }

    static authenticate(courseCode?: string): Promise<void> {
        return apiFetch(`/users/login/${courseCode || " "}`)
            .then(x => x.json())
            .then(x => {
                setToken(x.token);
                UserRepository.setCurrentCourse(x.courseCode);
            });
    }

    static updateCourse(course: Course, topics: Topic[]): Promise<CourseUser> {
        return apiFetch(`/users/courses/update/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                course: course,
                topics: topics
            })
        })
            .then(x => x.json());
    }

    static updateUserImage(newImage: string): Promise<User> {
        return apiFetch(`/users/me/image/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                image: newImage
            })
        }).then(x => x.json());
    }
}
