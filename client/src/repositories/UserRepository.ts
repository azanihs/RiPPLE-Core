import {
    CourseUser, User, Course,
    Notification, Topic, PeerConnection, Edge, UserSummary
} from "../interfaces/models";
import TopicRepository from "./TopicRepository";
import { setToken, apiFetch } from "./APIRepository";

let IDCounter = 0;
const types = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];
const engagementTypes = ["Competencies", "Goal Progress", "Achievements", "Recommendations", "Social Connections",
    "Study Partners", "Peers Mentored", "Questions Rated", "Questions Asked", "Questions Answered", "Questions Viewed"];

const _topics = ["Arrays", "Loops", "Recursion", "Algorithms", "Data Structures", "Variables"];

const _n = (i: number) => Math.floor(Math.random() * i);

const _icons = [
    "error",
    "supervisor_account",
    "bar_chart",
    "trending_up",
    "hourglass_full"
];

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
const notifications = Array.from({ length: notificationCount }).map((_, i: number) => ({
    id: i,
    name: getRandomTopic(),
    description: _notificationMessages[_n(_notificationMessages.length)],
    icon: _icons[_n(4)]
}));

const engagementNodes: Topic[] = engagementTypes.map((x, i) => ({
    id: 1000 + i,
    name: x
}));

type ServerEdge = {
    0: Topic,
    1: Topic,
    2: number,
    3: number
};

const userEngagementScores: ServerEdge[] = [];
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
    const getType = (i: number) => {
        return types[i] as "Provide Mentorship" | "Seek Mentorship" | "Find Study Partner";
    };

    const connections = new Array(2 + _n(8)).fill(0).map(_ => {
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
        _ => _topics[_n(_topics.length)]) as string[];

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

export default class UserRepository {
    static getLoggedInUser(): Promise<CourseUser> {
        return apiFetch<CourseUser>(`/users/me/`);
    }

    static getUserCourses(): Promise<Course[]> {
        return apiFetch<Course[]>(`/users/courses/`);
    }

    static getUserConnections(count: number): Promise<User[]> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(Array.from({ length: count }, makeUser));
            }, Math.random() * 1000);
        });
    }

    static getUserNotifications(): Promise<Notification[]> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(notifications);
            }, Math.random() * 1000);
        });
    }

    static getAllAvailableCategories(): Promise<string[]> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(types.slice());
            }, Math.random() * 1000);
        });
    }

    static getAllAvailableEngagementTypes(): Promise<Topic[]> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(engagementNodes);
            }, Math.random() * 1000);
        });
    }

    static getUserLeaderboard(sortField: string, sortOrder: "DESC" | "ASC"): Promise<UserSummary[]> {
        return apiFetch<UserSummary[]>(`/questions/leaderboard/${sortField}/${sortOrder}/`);
    }

    static getCompareAgainst(compareTo: string): Promise<Edge[]> {
        return apiFetch<ServerEdge[]>(`/questions/competencies/aggregate/${compareTo}/`)
        .then(x => x.map(x => {
            const edge: Edge = {
                source: TopicRepository.topicPointer(x[0]),
                target: TopicRepository.topicPointer(x[1]),
                competency: Math.round(x[2] * 100),
                attempts: Math.round(x[3] * 100)
            };
            return edge;
        }));
    }

    static getUserCompetencies(): Promise<Edge[]> {
        return apiFetch<ServerEdge[]>(`/questions/competencies/all/`)
            .then(x => x.map(x => {
                const edge: Edge = {
                    source: TopicRepository.topicPointer(x[0]),
                    target: TopicRepository.topicPointer(x[1]),
                    competency: Math.round(x[2] * 100),
                    attempts: Math.round(x[3] * 100)
                };
                return edge;
            }));
    }

    static getUserEngagement(): Promise<Edge[]> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(userEngagementScores.map(x => {
                    const edge: Edge = {
                        source: x[0] as Topic,
                        target: x[1] as Topic,
                        competency: Math.round(x[2]),
                        attempts: Math.round(x[3])
                    };
                    return edge;
                }));
            }, Math.random() * 1000);
        });
    }

    static getMeetingHistory(): Promise<{name: string, id: number }[]> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(["Toowong", "UQ", "University Of Queensland",
                    "Kenmore", "Indro"].map((x, i) => ({ name: x, id: i })));
            }, Math.random() * 1000);
        });
    }

    static getCurrentCourse(courseCode: string) {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(courseCode);
            }, Math.random() * 1000);
        });
    }

    static setCurrentToken(token: string) {
        setToken(token);
    }

    static authenticate(courseCode?: string): Promise<void> {
        return apiFetch<{token: string, courseCode: string}>(`/users/login/${courseCode || " "}`)
            .then(x => {
                setToken(x.token);
            });
    }

    static updateCourse(course: Course, topics: Topic[]): Promise<CourseUser> {
        return apiFetch<CourseUser>(`/users/courses/update/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                course: course,
                topics: topics
            })
        });
    }

    static updateUserImage(newImage: string): Promise<User> {
        return apiFetch<User>(`/users/me/image/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                image: newImage
            })
        });
    }
}
