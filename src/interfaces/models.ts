export interface Question {
    id: number,
    responseCount: number,

    difficulty: number,
    quality: number,

    topics: string[],
    images?: string[],
    content: string
}