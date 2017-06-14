export interface Question {
    id: number,
    rating: number,
    responseCount: number,
    difficulty: number,

    topic: string,
    title: string,
    content: string
}
export interface Peer {
    id: number,
    rating: number,

    title: string,
    content: string,
    topic: string 
}