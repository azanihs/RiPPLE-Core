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
        ][badge.id] || "priority_high"
    }
}