import { Badge, AcquiredBadge } from "../interfaces/models";
import faker from "faker";
const f: any = faker;

const getCategory: any = i => ["connections", "engagement", "competencies"][i];
const badges = Array.from({ length: 30 }, (x, i) => {
    return ({
        id: i,
        category: getCategory(f.random.number({ min: 0, max: 2 })),
        name: f.company.bsBuzz(),
        description: f.company.catchPhrase()
    });
});

const userBadges = badges
    .filter((_, i) => Math.random() < 0.5)
    .map((x: Badge, i) => {
        const acquiredBadge: AcquiredBadge = {
            id: i,
            badge: x,
            progress: Math.random() < 0.5 ? (Math.random() * 100) : -1,
            dateAcquired: new Date()
        };
        return acquiredBadge;
    });

export default class BadgeRepository {

    static getAllAvailableBadges(): Promise<Badge[]> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(badges.slice());
            }, Math.random() * 1000);
        });
    }

    static getAllUserBadges(): Promise<AcquiredBadge[]> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(userBadges.slice());
            }, Math.random() * 1000);
        });
    }
}
