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
            const phrase = new Array(20).fill(0).map(x => f.hacker.phrase()).join(" ");
            let questionContent = phrase;
            let images = [];
            if (Math.random() < 0.5) {
                if (Math.random() < 0.5) {
                    images = ['https://user-images.githubusercontent.com/16090868/27058555-56d1fa2a-5015-11e7-9d2c-6c38939afda4.png'];
                } else {
                    images = ['https://user-images.githubusercontent.com/16090868/27058529-3592fd64-5015-11e7-8d53-e1457ade0f6f.png'];

                }
            }

            const topicCount = f.random.number({min: 1, max: 4});
            const topics = new Array(topicCount).fill(0).map(x => f.hacker.abbreviation()) as string[];

            const question: Question = {
                id: i,
                responseCount: f.random.number({min: 0, max: 1000}),

                difficulty: f.random.number({min: 0, max: 10}),
                quality: f.random.number({min: 0, max: 10}),

                topics: topics,
                images: images,
                content: questionContent
            };
            return question;
        });
    }
}
