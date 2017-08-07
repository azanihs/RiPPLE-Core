export interface Question {
    id: number,
    responses: {
        author: Peer,
        upVotes: number,
        solution: number,
        content: string
    }[],

    difficulty: number,
    difficultyRepresentation: string,
    quality: number,

    topics: string[],
    images?: string[],
    content: string,

    solution: number,
    possibleAnswers: {
        id: number,
        content: string
    }[],
    explanation: string
}

export interface Peer {
    id: number,
    name: string,
    bio: string,

    proficiencies: string[],
    image: string,
    availableTimes: string[]
}

export interface User {
    id: number,
    self: Peer,

    connections: { // Should be replaced with PeerConnection[]
        id: number,
        type: string,
        topic: string,
        weight: number
    }[]
}

export interface UserSummary {
    name: string,
    reputation: number,
    questionsContributed: number,
    numberAnswers: number,
    numberComments: number
}

export interface Badge {
    id: number,
    name: string,
    category: "engagement" | "competencies" | "connections",
    description: string
}

export interface AcquiredBadge {
    badge: Badge,
    progress: number,
    dateAcquired: Date
}

export interface PeerConnection {
    edgeStart: number, // ID of edge start. Corresponds to a User ID
    edgeEnd: number, // ID of edge end. Corresponds to a User ID
    type: "Provide Mentorship" | "Seek Mentorship" | "Find Study Partner",
    topic: string,
    weight: number,
    date: Date, // Date the connection was made
}


