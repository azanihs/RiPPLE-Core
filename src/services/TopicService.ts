import { pushNotify, mergeCache } from "./Notify";
import TopicRepository from "../repositories/TopicRepository";

let topicCache = [];
export default class TopicService {

    static getAllAvailableTopics(notify?: Function) {
        //TODO: Fix race condition. Multiple components calling this at the same time could collide
        const originalLength = topicCache.length;
        TopicRepository.getAllAvailableTopics().then(topics => {
            topics.forEach(mergeCache(topicCache));
            if (originalLength !== topicCache.length) {
                pushNotify(notify, topicCache);
            }
        });

        return topicCache;
    }
}
