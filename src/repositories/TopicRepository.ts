import { Topic } from "../interfaces/models";

const topics = {};
export default class TopicRepository {

    static topicPointer(topic: Topic) {
        if (topics[topic.id] === undefined) {
            topics[topic.id] = topic;
        }
        return topics[topic.id];
    }

    static getAllAvailableTopics(): Promise<Topic[]> {
        return fetch("//localhost:8000/questions/topics/")
            .then(topics => topics.json())
            .then(topics => topics.map(x => TopicRepository.topicPointer(x)));
    }
}
