import "whatwg-fetch";
import { ITopic } from "../interfaces/models";
import { apiFetch } from "./APIRepository";

const topics: {[id: number]: ITopic} = {};
export default class TopicRepository {

    static topicPointer(topic: ITopic) {
        if (topics[topic.id] === undefined) {
            topics[topic.id] = topic;
        }
        return topics[topic.id];
    }

    static getAllAvailableTopics(): Promise<ITopic[]> {
        return apiFetch<ITopic[]>(`/questions/topics/`)
            .then(topics => topics.map(x => TopicRepository.topicPointer(x)));
    }
}
