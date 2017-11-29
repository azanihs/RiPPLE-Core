import { apiFetch } from "./APIRepository";
import { Question, Topic, QuestionUpload } from "../interfaces/models";
import TopicRepository from "./TopicRepository";

type SearchResult = { items: Question[], searchResult: any, totalItems: number, page: number };

function toQuestion(x: Question): Question {
    const question: Question = {
        id: x.id,
        difficulty: x.difficulty,
        quality: x.quality,
        solution: x.distractors.find(d => d.isCorrect === true),
        distractors: x.distractors,
        topics: x.topics.map(t => TopicRepository.topicPointer(t)),
        content: x.content,
        explanation: x.explanation,
        responses: x.responses,
        responseCount: x.responseCount
    };
    return question;
}

export default class QuestionRepository {
    static uploadQuestion(question: QuestionUpload): Promise<Question> {
        return apiFetch<Question>(`/questions/add/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify(question)
        })
            .then(x => x["question"])
            .then(response => toQuestion(response));
    }

    static getMany(count: number): Promise<Question[]> {
        return apiFetch<Question[]>(`/questions/all/`)
            .then(questions => questions.map(x => toQuestion(x)));
    }

    static search(sortField: string | undefined,
        sortOrder: string | undefined,
        filterField: string | undefined,
        filterTopics: string[] | undefined,
        query: string | undefined,
        page: string | undefined) {
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
                page
            })
        })
            .then(searchResult => ({
                totalItems: searchResult.totalItems,
                questions: searchResult.items.map(x => toQuestion(x)),
                page: searchResult.page
            }));
    }

    static submitResponse(distractorID: number) {
        return apiFetch<Object>(`/questions/respond/`, {
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
        return apiFetch<Object>(`/questions/rate/`, {
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

}
