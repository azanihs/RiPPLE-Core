import CacheService from "./CacheService";
import BadgeRepository from "../repositories/BadgeRepository";
import { pushNotify, every, mergeCache } from "./Notify";
import { Badge } from "../interfaces/models";

export default class BadgeService extends CacheService {
    static badgeToIcon(badge: Badge): string {
        return [
            "alarm",
            "assessment",
            "build",
            "change_history",
            "code",
            "compare_arrows",
            "delete",
            "done",
            "favorite",
            "event",
            "bug_report",
            "find_replace",
            "dns",
            "explore",
            "copyright",
            "explore",
            "gif",
            "language",
            "launch",
            "lightbulb_outline",
            "line_weight",
            "hourglass_empty",
            "home",
            "play_for_work",
            "polymer",
            "lock_open",
            "settings",
            "translate",
            "thumb_up",
            "trending_up",
            "toll"
        ][badge.id] || "priority_high";
    }

    static userHasBadge() {
        const subscriptionName = BadgeService.userHasBadge;
        const cache = BadgeService.getCache(subscriptionName).cache;

        BadgeRepository.getAllUserBadges()
            .then(badges => {
                if (badges.every(mergeCache(cache))) {
                    BadgeService.emit(subscriptionName, cache);
                }
            });
        BadgeService.emit(subscriptionName, cache);
    }

    static getAllAvailableBadges() {
        const subscriptionName = BadgeService.getAllAvailableBadges;
        const cache = BadgeService.getCache(subscriptionName).cache;

        BadgeRepository.getAllAvailableBadges()
            .then(badges => {
                if (every(badges)(mergeCache(cache))) {
                    BadgeService.emit(subscriptionName, cache);
                }
            });
        BadgeService.emit(subscriptionName, cache);
    }

    static getClosestUserBadges() {
        const subscriptionName = BadgeService.getClosestUserBadges;
        const cache = BadgeService.getCache(subscriptionName).cache;
        BadgeRepository.getAllUserBadges()
            .then(badges => badges.filter(x => x.progress > 0 && x.progress < 100)
                .sort((a, b) => (b.progress - a.progress))
                .slice(0, 3)
                .map(x => x.badge))
            .then(badges => {
                if (cache.length !== badges.length || badges.every((x, i) => x !== cache[i])) {
                    cache.splice(0, cache.length);
                    badges.forEach(badge => cache.push(badge));
                    BadgeService.emit(subscriptionName, cache);
                }
            });

        BadgeService.emit(subscriptionName, cache);
    }
}
