import { Badge } from "../interfaces/models";

export default class BadgeService {
    static badgeToIcon(badge: Badge): string {
        return [
            "alarm",
            "assessment",
            "build",
            "change_history",
            "code",
            "check_circle",
            "delete",
            "done",
            "favorite",
            "event"
        ][badge.id] || "priority_high"
    }
}