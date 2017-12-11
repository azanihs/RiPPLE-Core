import BadgeRepository from "../repositories/BadgeRepository";
import { IBadge } from "../interfaces/models";

export default class BadgeService {

    static badgeToIcon(badge: IBadge): string {
        return badge.icon;
    }

    static getAllUserBadges() {
        return BadgeRepository.getAllUserBadges();
    }

    static getBadgesByCategory(badges: IBadge[], category: string) {
        return badges.filter(x => x.category === category)
                .sort((a, b) => b.progress - a.progress);
    }

    static getClosestUserBadges(badges: IBadge[]) {
        return badges.filter(x => x.progress < 100)
                .sort((a, b) => (b.progress - a.progress))
                .slice(0, 3);
    }
}
