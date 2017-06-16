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
    rating: number,

    title: string,
    content: string,
    topic: string 
}