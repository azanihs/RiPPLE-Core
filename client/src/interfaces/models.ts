export interface Topic {
    id: number,
    name: string
};
export interface CompareSet {
    topics: Topic[], // Node List
    ownScores: Edge[], // Edge list of self
    compareAgainst: Edge[] // Edge list of other
};

export interface Question {
    id: number,
    difficulty: number,
    quality: number,

    topics: Topic[],

    content: string,
    explanation: string
    solution: Distractor,
    distractors: Distractor[],
    responseCount: number
};
export interface Distractor {
    id: number,
    content: string,
    isCorrect: boolean,
    response: string
}
export interface QuestionResponse {
    author: User,
    upVotes: number,
    solution: number,
    content: string
};

export interface Node {
    source: Topic,
    target: Topic,
    competency: number,
    attempts: number
};

export interface Course {
    courseCode: string,
    courseName: string,
    start?: number,
    end?: number,
    available?: boolean
};

export interface ReportQuestion {
    question: number,
    reason: string
};

export interface NetworkResponse {
    error?: string
}

export interface User {
    id: number,
    name: string,
    bio: string,
    image: string,

    proficiencies?: string[],
    availableTime?: Date,
    connections: PeerConnection[]
};

export interface CourseUser {
    user: User,
    course: Course,
    roles: string[],

    error?: string
};

export interface IConsentForm {
    content: string,
    author: CourseUser,

    error?: string
};

export interface IConsentUpload {
    payload?: AuthorResponse | undefined,
    author: CourseUser
};

export interface PeerConnection {
    edgeStart: number, // ID of edge start. Corresponds to a User ID
    edgeEnd: number, // ID of edge end. Corresponds to a User ID
    type: "Provide Mentorship" | "Seek Mentorship" | "Find Study Partner",
    topic: string,
    weight: number,
    date: Date, // Date the connection was made
    availableTime: Date
};

export interface UserSummary {
    name: string,
    image: string,
    reputation: number,

    questionsAuthored: number,
    questionsAnswered: number,
    questionsCommented: number,
    questionsViewed: number,
    questionsRated: number,

    connectionsMade: number,
    logins: number
};

export interface Badge {
    key: string,
    name: string,
    description: string,
    category: "engagement" | "competencies" | "connections",
    count: number,
    progress: number,
    icon: string,
    dateAcquired: Date
};

export interface Notification {
    id: number,
    name: string,
    description: string,
    icon: string
};

export interface Edge {
    source: Topic,
    target: Topic,
    competency: number,
    attempts: number
};

export interface QuestionBuilder {
    content: string,
    explanation: string,
    responses: {
        A: string,
        B: string,
        C: string,
        D: string
    },
    correctIndex: string,
    topics: Topic[]
};

export interface AuthorResponse {
    content: string,
    isCorrect: boolean,
    payloads: {
        [id: number]: string
    }
};

export interface QuestionUpload {
    question?: AuthorResponse,
    explanation?: AuthorResponse,
    responses: {
        A?: AuthorResponse,
        B?: AuthorResponse,
        C?: AuthorResponse,
        D?: AuthorResponse
    },
    topics?: Topic[]
};

export interface Day {
    id: number,
    day: string
}

export interface Time {
    id: number,
    start: {
        time: string,
        hour: number
    },
    end: {
        time: string,
        hour: number
    }
}

export interface Availability {
    id: number,
    courseUser: CourseUser,
    day: Day,
    time: Time
}

export interface CourseAvailability {
    courseUser: CourseUser,
    day: number,
    time: number,
    entries: number
};

export interface DayTime {
    day: number,
    time: number
};

export interface ILink {
    text: string,
    href: string
    icon: string
    submenu?: {
        text: string,
        href: string
    }[]
};

export interface IServerResponse<T> {
    error: string,
    notifications: Notification[]
    data: T
}

export interface StudyRole {
    id: number,
    role: string,
    description: string
}

export interface AvailableRole {
    courseUser: CourseUser,
    topic: Topic,
    studyRole: StudyRole
}

export interface StudyRole {
    id: number,
    role: string,
    description: string
}

export interface AvailableRole {
    courseUser: CourseUser,
    topic: Topic,
    studyRole: StudyRole
}
