import QuestionRepository from "../repositories/QuestionRepository";
import UserRepository from "../repositories/UserRepository";
import { IQuestion, IReportQuestion, ISearch } from "../interfaces/models";

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
    static search(searchQuery: ISearchQuery): Promise<{ questions: IQuestion[], totalItems: number, page: number }> {
        const { sortField, sortDesc, filterField, filterTopics, query, page, pageSize } = searchQuery;
        return QuestionRepository.search(sortField, sortDesc ? "DESC" : "ASC",
            filterField, filterTopics, query, page, pageSize);
    }

    static distributionForQuestion(question: IQuestion) {
        return QuestionRepository.getQuestionDistribution(question);
    }

    static submitResponse({ responseId }: { responseId: number }) {
        return QuestionRepository.submitResponse(responseId);
    }

    static submitRating({ responseId, rateType, rateValue }:
        { responseId: number, rateType: string, rateValue: number }) {
        return QuestionRepository.submitRating(responseId, rateType, rateValue);
    }

    static reportQuestion(questionId: number, reason: string[]) {
        const upload: IReportQuestion = {
            question: questionId,
            reason: reason
        };
        return QuestionRepository.uploadReport(upload);
    }

    static getReportReasons() {
        return QuestionRepository.getReportReasons();
    }

    static getQuestionById(questionId: number) {
        return QuestionRepository.getQuestionById(questionId);
    }

    static getRandomCourseQuestion() {
        return QuestionRepository.getRandomCourseQuestion();
    }

    static getSearchCacheForCourse() {
        return UserRepository.getSearchCacheForCourse();
    }
    static setSearchCacheForCourse(search: ISearch) {
        return UserRepository.setSearchCacheForCourse(search);
    }
}
