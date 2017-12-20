import {
    ICourseUser, IUser, ICourse, INotification, ITopic, IPeerConnection, ISearch,
    IEdge, IUserSummary, IEngagementType, IConsentForm, IConsentUpload
} from "../interfaces/models";
import TopicRepository from "./TopicRepository";
import { setToken, apiFetch, apiPost } from "./APIRepository";

let IDCounter = 0;
const types = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];

const _topics = ["Arrays", "Loops", "Recursion", "Algorithms", "Data Structures", "Variables"];

const _n = (i: number) => Math.floor(Math.random() * i);

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
    sortField: "recommended",
    sortDesc: true,
    filterField: "All Questions",
    query: "",
    page: 0,
    filterTopics: []
});

const _searchCaches: Map<string, ISearch> = new Map<string, ISearch>();
let _currentCourse = "";
const _userConsentMap: Map<string, boolean | undefined> = new Map<string, boolean | undefined>();
export default class UserRepository {
    static userHasConsentedForCourse(): Promise<boolean> {
        if (_userConsentMap.has(_currentCourse)) {
            return Promise.resolve(_userConsentMap.get(_currentCourse) !== undefined);
        } else {
            return apiFetch<boolean | undefined>(`/users/consent/`)
                .then(x => {
                    if (x !== undefined && typeof x !== "boolean") {
                        x = undefined;
                    }

                    _userConsentMap.set(_currentCourse, x);

                    return x !== undefined;
                });
        }
    }

    static getLoggedInUser(): Promise<ICourseUser> {
        return apiFetch<ICourseUser>(`/users/me/`);
    }

    static getConsentForm(): Promise<IConsentForm> {
        return apiFetch<IConsentForm>(`/users/consent_form/`);
    }

    static getUserConsentFormResponse(): Promise<boolean | undefined> {
        const cachedUserConsent = _userConsentMap.get(_currentCourse);
        if (cachedUserConsent !== undefined) {
            return Promise.resolve(cachedUserConsent);
        }

        return apiFetch<boolean | undefined>(`/users/consent/`)
            .then(x => {
                if (x === undefined || typeof x == "boolean") {
                    return x;
                }
                return undefined;
            });
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
        return apiFetch<INotification[]>(`/users/notifications/all/`);
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
            .then(topics => topics.map(x => TopicRepository.engagementPointer(x)));
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

    static uploadConsentForm(consentForm: IConsentUpload): Promise<string> {
        return apiFetch<string>(`/users/submit_consent_form/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify(consentForm)
        });
    }

    static sendConsent(response: boolean): Promise<boolean> {
        _userConsentMap.set(_currentCourse, response);
        return apiFetch<{response: boolean}>(`/users/consent/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({ "response": response })
        })
            .then(function(x) {
                return x.response;
            });
    }
}
