import QuestionRepository from "../repositories/QuestionRepository";
import { Question } from "../interfaces/models";

export default class QuestionService {
    static search(searchQuery): Promise<Question[]> {
        const { sortField, sortDesc, filterField, query } = searchQuery;
        return QuestionRepository.search(sortField || "", sortDesc ? "DESC" : "ASC", filterField || "", query || "");
    }

    static getRecommendedForUser({ count }: { count: number }): Promise<Question[]> {
        return QuestionRepository.getMany(count);
    }

    static distributionForQuestion(question: Question) {
        const numberAnswers = question.distractors.length;
        const distribution = new Map();
        const distributionSum = 0;
        for (let i = 0; i < numberAnswers; i++) {
            const responseDistribution = Math.random() / 2;
            if (Math.abs(responseDistribution - distributionSum) < 0 || i == numberAnswers - 1) {
                distribution.set(question.distractors[i], Math.abs(distributionSum - responseDistribution));
            } else {
                distribution.set(question.distractors[i], responseDistribution);
            }
        }
        return distribution;
    }
}
