import {
    ICourseUser, IUser, ICourse, ISearch,
    INotification, ITopic, IPeerConnection, IEdge, IUserSummary, IEngagementType, IConsentForm
} from "../interfaces/models";
import TopicRepository from "./TopicRepository";
import { setToken, apiFetch, apiPost } from "./APIRepository";

let IDCounter = 0;
const types = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];

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

type IServerEdge = {
    0: ITopic,
    1: ITopic,
    2: number,
    3: number
};

const makeUser = () => {
    const getType = (i: number) => {
        return types[i] as "Provide Mentorship" | "Seek Mentorship" | "Find Study Partner";
    };

    const connections = new Array(2 + _n(8)).fill(0).map(_ => {
        const connection: IPeerConnection = {
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

    const user: IUser = {
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

const _defaultSearch = () => ({
    sortField: "",
    sortDesc: false,
    filterField: "All Questions",
    query: "",
    page: 0,
    filterTopics: []
});

const _searchCaches: Map<string, ISearch> = new Map<string, ISearch>();
let _currentCourse: string = "";

const _hasConsentedMap: Map<string, boolean> = new Map<string, boolean>();
export default class UserRepository {
    static userHasConsentedForCourse(): Promise<boolean> {
        if (_hasConsentedMap.has(_currentCourse)) {
            return Promise.resolve(_hasConsentedMap.get(_currentCourse)!);
        } else {
            return apiFetch<boolean>(`/users/has_consented/`)
                .then(x => {
                    _hasConsentedMap.set(_currentCourse, x);
                    return x;
                });
        }
    }

    static getLoggedInUser(): Promise<ICourseUser> {
        return apiFetch<ICourseUser>(`/users/me/`);
    }

    static getConsentForm(): Promise<IConsentForm> {
        return apiFetch<IConsentForm>(`/users/consent_form`);
    }

    static getUserCourses(): Promise<ICourse[]> {
        return apiFetch<ICourse[]>(`/users/courses/`);
    }

    static getUserConnections(count: number): Promise<IUser[]> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(Array.from({ length: count }, makeUser));
            }, Math.random() * 1000);
        });
    }

    static getUserNotifications(): Promise<INotification[]> {
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

    static getAllAvailableEngagementTypes(): Promise<IEngagementType[]> {
        return apiFetch<IEngagementType[]>(`/users/engagement/`)
            .then(topics => topics.map(x => TopicRepository.topicPointer(x)));
    }

    static getUserLeaderboard(sortField: string, sortOrder: "DESC" | "ASC"): Promise<IUserSummary[]> {
        return apiFetch<IUserSummary[]>(`/questions/leaderboard/${sortField}/${sortOrder}/`);
    }

    static getCompareAgainst(compareTo: string): Promise<IEdge[]> {
        return apiFetch<IServerEdge[]>(`/questions/competencies/aggregate/${compareTo}/`)
        .then(x => x.map(x => {
            const edge: IEdge = {
                source: TopicRepository.topicPointer(x[0]),
                target: TopicRepository.topicPointer(x[1]),
                competency: Math.round(x[2] * 100),
                attempts: Math.round(x[3] * 100)
            };
            return edge;
        }));
    }

    static getUserCompetencies(): Promise<IEdge[]> {
        return apiFetch<IServerEdge[]>(`/questions/competencies/all/`)
            .then(userEngagement => userEngagement.map(x => {
                const edge: IEdge = {
                    source: TopicRepository.topicPointer(x[0]),
                    target: TopicRepository.topicPointer(x[1]),
                    competency: Math.round(x[2] * 100),
                    attempts: Math.round(x[3] * 100)
                };
                return edge;
            }));
    }

    static getEngagementAgainst(compareTo: string): Promise<IEdge[]> {
        return apiFetch<IServerEdge[]>(`/users/engagement/aggregate/${compareTo}/`)
            .then(aggregateEngagement => aggregateEngagement.map(x => {
                const edge: IEdge = {
                    source: TopicRepository.engagementPointer(x[0]),
                    target: TopicRepository.engagementPointer(x[1]),
                    competency: Math.round(x[2] * 100),
                    attempts: Math.round(x[3] * 100)
                };
                return edge;
            }));
    }

    static getUserEngagement(): Promise<IEdge[]> {
        return apiFetch<IServerEdge[]>(`/users/engagement/all/`)
            .then(userEngagementScores => userEngagementScores.map(x => {
                const edge: IEdge = {
                    source: TopicRepository.engagementPointer(x[0]),
                    target: TopicRepository.engagementPointer(x[1]),
                    competency: Math.round(x[2] * 100),
                    attempts: Math.round(x[3] * 100)
                };
                return edge;
            }));
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
                _currentCourse = x.courseCode;
            });
    }

    static getSearchCacheForCourse() {
        const cache = _searchCaches.get(_currentCourse);
        if (!cache) {
            _searchCaches.set(_currentCourse, _defaultSearch());
        }
        return Promise.resolve(_searchCaches.get(_currentCourse)!);
    }

    static setSearchCacheForCourse(search: ISearch) {
        const arrCopy = search.filterTopics.slice();
        _searchCaches.set(_currentCourse, Object.assign({}, search, { filterTopics: arrCopy }));
    }

    static updateCourse(course: ICourse, topics: ITopic[]): Promise<ICourseUser> {
        return apiPost<ICourseUser>(`/users/courses/update/`, { course, topics });
    }

    static updateUserImage(newImage: string): Promise<IUser> {
        return apiPost<IUser>(`/users/me/image/`, {
            image: newImage
        });
    }

    static uploadConsentForm(consentForm: IConsentForm): Promise<IConsentForm> {
        return apiFetch<{consentForm: IConsentForm}>(`/users/submit_consent_form/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify(consentForm)
        })
            .then(x => x.consentForm);
    }

    static sendConsent(response: boolean): Promise<string> {
        return apiFetch<{response: string}>(`/users/consent/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({ "response": response })
        })
            .then(function(x) {
                _hasConsentedMap.set(_currentCourse, true);
                return x.response;
            });
    }
}
