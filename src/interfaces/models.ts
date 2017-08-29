export interface Topic {
    id: number,
    name: string
};

export interface Question {
    id: number,
    difficulty: number,
    quality: number,

    topics: Topic[],

    content: string,
    explanation: string
    solution: number,
    distractors: {
        id: number,
        content: string,
        isCorrect: boolean,
        response: string
    }[],

    responses: QuestionResponse[]
};

export interface QuestionResponse {
    author: User,
    upVotes: number,
    solution: number,
    content: string
};

export interface User {
    id: number,
    name: string,
    bio: string,
    image: string,

    proficiencies?: string[],
    availableTime?: Date,
    connections: PeerConnection[]
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
    questionsContributed: number,
    numberAnswers: number,
    numberComments: number
};

export interface Badge {
    id: number,
    name: string,
    category: "engagement" | "competencies" | "connections",
    description: string
};

export interface AcquiredBadge {
    badge: Badge,
    progress: number,
    dateAcquired: Date
};

export interface Notification {
    id: number,
    type: "Incoming Connection" | "Achievement" | "Personal Goal" | "Upcoming Meeting",
    content: string,
    read: boolean
};
