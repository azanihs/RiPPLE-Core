import { apiFetch, apiPost } from "./APIRepository";
import { IQuestion, IQuestionUpload, IDistractor, INetworkResponse, IReportQuestion, IReasonList } from "../interfaces/models";
import TopicRepository from "./TopicRepository";

type ISearchResult = { items: IQuestion[], searchResult: any, totalItems: number, page: number };

function toQuestion(x: IQuestion): IQuestion {
    let solution: undefined | IDistractor = x.distractors.find(d => d.isCorrect === true);
    if (solution === undefined) {
        throw new Error(`Question id: ${x.id} does not have a solution`);
    }

    const question: IQuestion = {
        id: x.id,
        difficulty: Math.round(x.difficulty),
        quality: Math.round(x.quality),
        topics: x.topics.map(t => TopicRepository.topicPointer(t)),
        content: x.content,
        explanation: x.explanation,
        solution: solution,
        distractors: x.distractors,
        responseCount: x.responseCount
    };
    return question;
}

export default class QuestionRepository {
    static uploadQuestion(question: IQuestionUpload): Promise<IQuestion> {
        return apiPost<{question: IQuestion}>(`/questions/add/`, question)
            .then(x => x.question)
            .then(response => toQuestion(response));
    }

    static search(sortField: string | undefined,
        sortOrder: string | undefined,
        filterField: string | undefined,
        filterTopics: number[] | undefined,
        query: string | undefined,
        page: number | undefined,
        pageSize: number | undefined) {
        return apiPost<ISearchResult>(`/questions/search/`, {
            sortField,
            sortOrder,
            filterField,
            filterTopics,
            query,
            page,
            pageSize
        })
        .then(searchResult => ({
            totalItems: searchResult.totalItems,
            questions: searchResult.items.map(x => toQuestion(x)),
            page: searchResult.page
        }));
    }

    static submitResponse(distractorID: number) {
        return apiPost<{}>(`/questions/respond/`, { distractorID });
    }

    static submitRating(distractorID: number, rateType: string, rateValue: number) {
        return apiPost<{}>(`/questions/rate/`, {
            distractorID: distractorID,
            [`${rateType}`]: rateValue
        });
    }

    static getQuestionDistribution(question: IQuestion): Promise<{[responseId: number]: number}> {
        return apiFetch(`/questions/distribution/${question.id}/`);
    }

    static uploadReport(questionReport: IReportQuestion) {
        return apiPost<INetworkResponse>("/questions/report/", { questionReport });
    }

    static getQuestionById(questionId: number) {
        return apiFetch<IQuestion>(`/questions/id/${questionId}/`)
            .then(toQuestion);
    }
    static getRandomCourseQuestion() {
        return apiFetch<number>(`/questions/random/`);
    }

    static getReportReasons() {
        return apiFetch<IReasonList>("/questions/reasons/", {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "Application/json"
            })
        }).then(x => x.reasonList);
    }
}
