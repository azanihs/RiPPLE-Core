import BadgeRepository from "../repositories/BadgeRepository";
import { Badge } from "../interfaces/models";

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

    static userHasBadge({ badgeId }: { badgeId: number }) {
        return BadgeRepository.getAllUserBadges()
            .then(badges => badges.find(userBadge => userBadge.badge.id === badgeId));
    }

    static getAllAvailableBadges() {
        return BadgeRepository.getAllAvailableBadges();
    }

    static getBadgesByCategory({ category }: { category: string }) {
        return BadgeRepository.getAllAvailableBadges()
            .then(badges => badges.filter(x => x.category === category));
    }


    static getClosestUserBadges() {
        return BadgeRepository.getAllUserBadges()
            .then(badges => badges.filter(x => x.progress > 0 && x.progress < 100)
                .sort((a, b) => (b.progress - a.progress))
                .slice(0, 3)
                .map(x => x.badge));
    }
}
