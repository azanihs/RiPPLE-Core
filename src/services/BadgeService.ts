import { Badge } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";

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

    static getAllAvailableBadges() {
        return UserRepository.getAllAvailableBadges();
    }

    static getBadgeByType(category: string) {
        return UserRepository.getAllAvailableBadges().filter(x => x.category == category);
    }

    static getClosestUserBadges() {
        return UserRepository.getAllUserBadges()
            .filter(x => x.progress > 0 && x.progress < 100)
            .sort((a, b) => (b.progress - a.progress))
            .slice(0, 3)
            .map(x => x.badge);
    }
}
