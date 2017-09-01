import CacheService from "./CacheService";
import TopicRepository from "../repositories/TopicRepository";

import { pushNotify, every, mergeCache } from "./Notify";

let topicCache = [];
export default class TopicService {

    static getAllAvailableTopics(notify?: Function) {
        const subscriptionName = TopicService.userHasBadge;
        const cache = BadgeService.getCache(subscriptionName).cache;
        const emitFn = (badge: Badge) => cache.find(x => x.badge === badge);

        BadgeRepository.getAllUserBadges()
            .then(badges => {
                if (badges.every(mergeCache(cache))) {
                    BadgeService.emit(subscriptionName, emitFn);
                }
            });
        BadgeService.emit(subscriptionName, emitFn);

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
