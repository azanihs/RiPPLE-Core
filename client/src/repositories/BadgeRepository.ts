import { Badge, AcquiredBadge } from "../interfaces/models";
const _n = i => Math.floor(Math.random() * i);
const getCategory: any = i => ["connections", "engagement", "competencies"][i];

// From: https://meta.stackexchange.com/questions/67397/list-of-all-badges-with-full-descriptions#67399
const _badgeTitles = ["Bronze", "Gold", "Silver", "Monkey", "Spider", "Web", "Bell", "Tumbleweed", "Bugs",
    "Consistent", "Always there", "Computer Whiz", "On It", "Lead", "Elephant"];
const _badgeDescriptions = [
    "Bronze; Awarded when you get three achievements",
    "Gold; Awarded when you get ten achievements",
    "Silver; Awarded when you get five achievements",
    "Earnt by authoring twenty questions",
    "Earnt by reporting fifteen questions",
    "Answering twenty questions earns you this award",
    "Rated at least ten questions",
    "Was absent all semester",
    "Collects bugs!",
    "Answer a question each day for a week",
    "Log on each day for a year",
    "Authored a question",
    "Made a social connection",
    "Made it into the top ten on the leaderboard",
    "Rejected a social connection"
];

const badges = _badgeTitles.map((name, i) => {
    return {
        id: i,
        category: getCategory(_n(2)),
        name: name,
        description: _badgeDescriptions[i]
    };
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
