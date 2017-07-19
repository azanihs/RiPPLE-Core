import QuestionRepository from "../repositories/QuestionRepository";

export default class QuestionService {
    static getQuestion(type: string) {
        return QuestionRepository.getMany(1)[0];
    }
}