import { Question, Topic } from "../interfaces/models";
import PeerRepository from "./PeerRepository";
import f from "faker";

const topics = {};
export default class QuestionRepository {
    static getMany(count: number): Promise<Question[]> {
        return fetch("//localhost:8000/questions/all")
            .then(questions => questions.json())
            .then(questions => questions.map(x => {
                const question: Question = {
                    id: x.id,
                    difficulty: x.difficulty,
                    quality: x.quality,
                    solution: x.distractors.find(d => d.isCorrect === true),
                    distractors: x.distractors,
                    topics: x.topics.map(t => {
                        let topic: Topic = topics[t.id];
                        if (topic === undefined) {
                            topic = {
                                id: t.id,
                                name: t.name
                            };
                            topics[t.id] = topic;
                        }
                        return topics[t.id];
                    }),

                    content: x.content,
                    explanation: x.explanation,

                    responses: []
                };

                return question;
            }));
    }

    static getAllAvailableTopics(): Promise<Topic[]> {
        return QuestionRepository.getMany(25)
            .then(questions => questions.reduce((a: Topic[], b: Question) => a.concat(b.topics), []));
    }

}
