export interface Question {
    id: number,
    responseCount: number,

    difficulty: number,
    quality: number,

    topic: string,
    content: string
}