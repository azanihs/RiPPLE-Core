import QuestionRepository from "../repositories/QuestionRepository";
import { Question } from "../interfaces/models";

export default class QuestionService {
    static getQuestion(type: string) {
        return QuestionRepository.getMany(1)[0];
    }

    static distributionForQuestion(question: Question) {
        const numberAnswers = question.possibleAnswers.length;
        const distribution = new Map();
        const distributionSum = 0;
        for (let i = 0; i < numberAnswers; i++) {
            const responseDistribution = Math.random() / 2;
            if (Math.abs(responseDistribution - distributionSum) < 0 || i == numberAnswers - 1) {
                distribution.set(question.possibleAnswers[i], Math.abs(distributionSum - responseDistribution));
            } else {
                distribution.set(question.possibleAnswers[i], responseDistribution)
            }
        }
        return distribution;
    }
}