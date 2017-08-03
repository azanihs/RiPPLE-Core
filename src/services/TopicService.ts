import QuestionRepository from "../repositories/UserRepository";

export default class TopicService {
    static getAllAvailableTopics(): string[] {
        return QuestionRepository.getAllAvailableTopics();
    }
}
