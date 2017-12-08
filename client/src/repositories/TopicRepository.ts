import { ITopic, IEngagementType } from "../interfaces/models";
import { apiFetch } from "./APIRepository";

const _topics: {[id: number]: ITopic} = {};
const _engagements: {[id: number]: IEngagementType} = {};

export default class TopicRepository {

    static engagementPointer(engagement: IEngagementType) {
        if (_engagements[engagement.id] === undefined) {
            _engagements[engagement.id] = engagement;
        }
        return _engagements[engagement.id];
    }

    static topicPointer(topic: ITopic) {
        if (_topics[topic.id] === undefined) {
            _topics[topic.id] = topic;
        }
        return _topics[topic.id];
    }

    static getAllAvailableTopics(): Promise<ITopic[]> {
        return apiFetch<ITopic[]>(`/questions/topics/`)
            .then(topics => topics.map(x => TopicRepository.topicPointer(x)));
    }
}
