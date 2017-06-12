import { Question } from "../interfaces/models";
import faker from "faker";

const f = faker as any;
export default class QuestionRepository {

    /**
     * Returns a
     * @param count The number of questions to return
     * @return Question[]
     */
    static getMany(count: number): Question[] {
        return new Array(count).fill(0).map((_, i) => {
            let questionContent = f.hacker.phrase() + " " + f.hacker.phrase();

            const question: Question = {
                id: i,
                responseCount: f.random.number({min: 0, max: 1000}),

                difficulty: f.random.number({min: 0, max: 10}),
                quality: f.random.number({min: 0, max: 10}),

                topic: f.hacker.abbreviation(),
                content: questionContent
            };
            return question;
        });
    }
}
