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
    time: Date
}