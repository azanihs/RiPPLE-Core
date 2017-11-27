import BadgeRepository from "../repositories/BadgeRepository";
import { Badge } from "../interfaces/models";

export default class BadgeService {
    static badgeToIcon(badge: Badge): string {
        if (badge.name == "Advanced Question Author") {
            return "alarm";
        } else if (badge.name == "Intermediate Question Author") {
            return "assessment";
        } else if (badge.name == "Beginner Question Author") {
            return "build";
        } else if (badge.name == "Advanced Response") {
            return "change_history";
        } else if (badge.name == "Intermediate Response") {
            return "code";
        } else if (badge.name == "Beginner Response") {
            return "compare_arrows";
        }
        
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
        ][badge.key] || "priority_high";
    }

    static userHasBadge({ badgeId }: { badgeId: string }) {
        return BadgeRepository.getAllUserBadges()
            .then(badges => badges.find(userBadge => userBadge.key === badgeId));
    }

    static getAllUserBadges() {
        return BadgeRepository.getAllUserBadges();
    }

    static getBadgesByCategory(badges: Badge[], category: string) {
        return badges.filter(x => x.category === category);
    }


    static getClosestUserBadges(badges: Badge[]) {
        return badges.filter(x => x.progress > 0 && x.progress < 100)
                .sort((a, b) => (b.progress - a.progress))
                .slice(0, 3);
    }
}
