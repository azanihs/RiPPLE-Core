import QuestionRepository from "../repositories/QuestionRepository";

export default class TopicService {
    static topics = [];

    static getAllAvailableTopics() {
        const update = QuestionRepository.getAllAvailableTopics()
            .then(topics => {
                topics.forEach(x => {
                    if (TopicService.topics.find(t => t.id === x.id) === undefined) {
                        TopicService.topics.push(x);
                    }
                });
            });

        return TopicService.topics;
    }
}
