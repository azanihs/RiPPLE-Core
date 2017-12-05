import QuestionRepository from "../repositories/QuestionRepository";
import { Question } from "../interfaces/models";

interface ISearchQuery {
    sortField?: string,
    sortDesc?: "ASC" | "DESC",
    filterField?: string,
    filterTopics?: number[],
    query?: string,
    page?: number,
    pageSize?: number
};

export default class QuestionService {
    static search(searchQuery: ISearchQuery): Promise<{ questions: Question[], totalItems: number, page: number }> {
        const { sortField, sortDesc, filterField, filterTopics, query, page, pageSize } = searchQuery;
        return QuestionRepository.search(sortField, sortDesc ? "DESC" : "ASC",
            filterField, filterTopics, query, page, pageSize);
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

}
