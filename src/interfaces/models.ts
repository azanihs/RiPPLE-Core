export interface Question {
    id: number,
    rating: number,
    responseCount: number,
    difficulty: number,

    topic: string,
    title: string,
    content: string
}