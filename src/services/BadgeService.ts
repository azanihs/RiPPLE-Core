import { pushNotify, mergeCache } from "./Notify";
import { Badge } from "../interfaces/models";
import BadgeRepository from "../repositories/BadgeRepository";

const cachedBadges = [];
const cachedUserAquiredBadges = [];
const cachedClosestUserBadges = [];

export default class BadgeService {
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

    static userHasBadge(badgeId, notify?: Function) {
        BadgeRepository.getAllUserBadges()
            .then(badges => {
                const originalLength = cachedUserAquiredBadges.length;
                badges.forEach(mergeCache(cachedUserAquiredBadges));
                if (originalLength !== cachedUserAquiredBadges.length) {
                    pushNotify(notify, cachedUserAquiredBadges.find(x => x.badge.id == badgeId));
                }
            });

        return cachedUserAquiredBadges.find(x => x.badge.id === badgeId);
    }

    static getAllAvailableBadges(notify?: Function) {
        BadgeRepository.getAllAvailableBadges()
            .then(badges => {
                const originalLength = cachedBadges.length;
                badges.forEach(mergeCache(cachedBadges));
                if (originalLength !== cachedBadges.length) {
                    pushNotify(notify, cachedBadges);
                }
            });

        return cachedBadges;
    }

    static getBadgeByType(category: string, notify?: Function) {
        const badgeFilter = x => x.category === category;
        const originalLength = cachedBadges.length;

        BadgeRepository.getAllAvailableBadges()
            .then(badges => {
                badges.forEach(mergeCache(cachedBadges));
                if (originalLength !== cachedBadges.length) {
                    pushNotify(notify, cachedBadges.filter(badgeFilter));
                }
            });
        return cachedBadges.filter(badgeFilter);
    }

    static getClosestUserBadges(notify?: Function) {
        const originalCache = cachedClosestUserBadges.slice();

        BadgeRepository.getAllUserBadges()
            .then(badges => badges.filter(x => x.progress > 0 && x.progress < 100)
                .sort((a, b) => (b.progress - a.progress))
                .slice(0, 3)
                .map(x => x.badge))
            .then(badges => {
                cachedClosestUserBadges.splice(0, cachedClosestUserBadges.length);
                badges.forEach(badge => cachedClosestUserBadges.push(badge));

                if (!originalCache.every((x, i) => originalCache.length === cachedClosestUserBadges.length
                    && originalCache[i] === cachedClosestUserBadges[i])) {
                    pushNotify(notify, cachedClosestUserBadges);
                }
            });

        return cachedClosestUserBadges;
    }
}
