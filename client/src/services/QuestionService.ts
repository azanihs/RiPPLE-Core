import QuestionRepository from "../repositories/QuestionRepository";
import { Question, ReportQuestion } from "../interfaces/models";

export default class QuestionService {
    static search(searchQuery): Promise<{ questions: Question[], totalItems: number, page: number }> {
        const { sortField, sortDesc, filterField, filterTopics, query, page } = searchQuery;
        return QuestionRepository.search(sortField, sortDesc ? "DESC" : "ASC", filterField, filterTopics, query, page);
    }

    static getRecommendedForUser({ count }: { count: number }): Promise<Question[]> {
        return QuestionRepository.getMany(count);
    }

    static distributionForQuestion(question: Question) {
        return QuestionRepository.getQuestionDistribution(question);
    }

    static submitResponse({ responseId }: { responseId: number }) {
        return QuestionRepository.submitResponse(responseId);
    }

    static submitRating({ responseId, rateType, rateValue }:
        { responseId: number, rateType: string, rateValue: number }) {
        return QuestionRepository.submitRating(responseId, rateType, rateValue);
    }

    static reportQuestion(question: Question, reason: string) {
        const upload: ReportQuestion = {
            question: undefined,
            reason: undefined
        };

        upload.question = question.id;
        upload.reason = reason;

        QuestionRepository.uploadReport(upload);
    }

}
