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
            let questionTitle = f.company.catchPhrase();
            let questionContent = f.hacker.phrase();

            const question: Question = {
                id: i,
                rating: f.random.number({min: 0, max: 5}),
                responseCount: f.random.number({min: 0, max: 1000}),
                difficulty: f.random.number({min: 0, max: 10}),

                title: questionTitle,
                topic: f.hacker.abbreviation(),
                content: questionContent
            };
            return question;
        });
    }
}
