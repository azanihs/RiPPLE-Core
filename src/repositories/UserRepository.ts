import { User, Peer, Badge, AcquiredBadge } from "../interfaces/models";
import PeerRepository from "./PeerRepository";
import f from "faker";

let IDCounter = 0;
const types = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];
const getCategory: any = i => {
    return ["connections", "engagement", "competencies"][i];
}

const topics = new Array(10).fill(0).map(x => f.hacker.abbreviation()).filter((x, i, self) => self.indexOf(x) == i);
const badges = new Array(30).fill(0).map((x, i) => ({
    id: i,
    category: getCategory(f.random.number({ min: 0, max: 2 })),
    name: f.company.bsBuzz(),
    description: f.company.catchPhrase()
}));

const userBadges = badges
    .filter((_, i) => Math.random() < 0.5)
    .map((x: Badge) => {
        const acquiredBadge: AcquiredBadge = {
            badgeId: x.id,
            progress: Math.random() < 0.5 ? (Math.random() * 100) : -1,
            dateAcquired: new Date()
        };
        return acquiredBadge;
    });

export default class UserRepository {

    /**
     * Returns an array of Peer objects
     * @param {number} peerCount The number of peers to return
     * @return {Peer[]} An array of Peers with length peerCount
     */
    static getLoggedInUser(): User {
        const peer: Peer = PeerRepository.getMany(1)[0];
        const connections = new Array(f.random.number({ min: 2, max: 10 })).fill(0).map(x => {
            const connection = {
                id: IDCounter++,
                type: types[f.random.number({ min: 0, max: 2 })],
                topic: topics[f.random.number({ min: 0, max: 10 })],
                weight: f.random.number({ min: 0, max: 10 })
            }
            return connection;
        });

        const user: User = {
            id: IDCounter++,
            self: peer,
            connections: connections
        };

        return user;
    }

    static getAllAvailableBadges(): Badge[] {
        return badges.slice()
    }
    static getAllUserBadges(): AcquiredBadge[] {
        return userBadges.slice();
    }

    static getAllAvailableCategories(): string[] {
        return types.slice()
    }
    static getAllAvailableTopics(): string[] {
        return topics.slice();
    }
}