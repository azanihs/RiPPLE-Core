import { apiFetch } from "./APIRepository";
import { Question, QuestionUpload, Distractor, NetworkResponse,
    ReportQuestion, ReasonList } from "../interfaces/models";
import TopicRepository from "./TopicRepository";

type SearchResult = { items: Question[], searchResult: any, totalItems: number, page: number };

function toQuestion(x: Question): Question {
    let solution: undefined | Distractor = x.distractors.find(d => d.isCorrect === true);
    if (solution === undefined) {
        throw new Error(`Question id: ${x.id} does not have a solution`);
    }

    const question: Question = {
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
    static uploadQuestion(question: QuestionUpload): Promise<Question> {
        return apiFetch<{question: Question}>(`/questions/add/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify(question)
        })
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
        return apiFetch<SearchResult>(`/questions/search/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                sortField,
                sortOrder,
                filterField,
                filterTopics,
                query,
                page,
                pageSize
            })
        })
            .then(searchResult => ({
                totalItems: searchResult.totalItems,
                questions: searchResult.items.map(x => toQuestion(x)),
                page: searchResult.page
            }));
    }

    static submitResponse(distractorID: number) {
        return apiFetch<{}>(`/questions/respond/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                distractorID: distractorID
            })
        });
    }

    static submitRating(distractorID: number, rateType: string, rateValue: number) {
        return apiFetch<{}>(`/questions/rate/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                distractorID: distractorID,
                [`${rateType}`]: rateValue
            })
        });
    }

    static getQuestionDistribution(question: Question): Promise<{[responseId: number]: number}> {
        return apiFetch(`/questions/distribution/${question.id}/`);
    }

    static uploadReport(questionReport: ReportQuestion) {
        return apiFetch<NetworkResponse>("/questions/report/", {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "Application/json"
            }),
            body: JSON.stringify({
                questionReport
            })
        });
    }

    static getReportReasons() {
        return apiFetch<ReasonList>("/questions/reasons/", {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "Application/json"
            })
        }).then(x => x.reasonList);
    }
}
