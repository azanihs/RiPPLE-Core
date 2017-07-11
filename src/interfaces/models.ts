export interface Question {
    id: number,
    responseCount: number,

    difficulty: number,
    quality: number,

    topics: string[],
    images?: string[],
    content: string
}

export interface Peer {
    id: number,
    name: number,
    bio: string,

    proficiencies: string[],
    image: string,
    availableTimes: string[]
}

export interface User {
    id: number,
    self: Peer,

    connections: {
        id: number,
        type: string,
        topic: string,
        weight: number
    }[]
}

export interface Badge {
    id: number,
    name: string,
    description: string
}
export interface AcquiredBadge {
    badgeId: number,
    dateAcquired: Date
}