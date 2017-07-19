import { Question } from "../interfaces/models";
import PeerRepository from "./PeerRepository";
import f from "faker";

export default class QuestionRepository {

    /**
     * Returns a collection of questions
     * @param {number} count The number of questions to return
     * @return {Question[]} An array of questions with length equal to count
     */
    static getMany(count: number): Question[] {
        return new Array(count).fill(0).map((_, i) => {
            const questionContent = new Array(20).fill(0).map(x => f.hacker.phrase()).join(" ");
            const images = Math.random() < 0.5 ? [f.image.image()] : []

            const topicCount = f.random.number({ min: 2, max: 4 });
            const topics = new Array(topicCount).fill(0).map(x => f.hacker.abbreviation()) as string[];

            const question: Question = {
                id: i,
                responses: new Array(Math.floor(Math.random() * 500)).fill(0).map(x => ({
                    author: PeerRepository.getMany(1)[0],
                    upVotes: Math.floor(Math.random() * 100),
                    solution: Math.floor(Math.random() * 4),
                    content: new Array(10).fill(0).map(x => f.hacker.phrase()).join(" ")
                })),
                difficulty: f.random.number({ min: 0, max: 10 }),
                quality: f.random.number({ min: 0, max: 10 }),

                topics: topics,
                images: images,
                content: questionContent,

                possibleAnswers: new Array(4).fill(0).map((x, i) => ({
                    id: i,
                    content: new Array(2).fill(0).map(x => f.hacker.phrase()).join(" ")
                })),
                solution: Math.floor(Math.random() * 4),
                explanation: new Array(10).fill(0).map(x => f.hacker.phrase()).join(" ")
            };
            return question;
        });
    }
}
