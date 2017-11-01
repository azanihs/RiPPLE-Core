import TopicRepository from "../repositories/TopicRepository";

export default class TopicService {

    static getAllAvailableTopics() {
        return TopicRepository.getAllAvailableTopics();
    }
}
