import { User, Peer, Badge, AcquiredBadge } from "../interfaces/models";
import PeerRepository from "./PeerRepository";
import f from "faker";

let IDCounter = 0;
const categories = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];
const topics = new Array(10).fill(0).map(x => f.hacker.abbreviation()).filter((x, i, self) => self.indexOf(x) == i);
const badges = new Array(10).fill(0).map((x, i) => ({
    id: i,
    name: f.company.bsBuzz(),
    description: f.company.catchPhrase()
}));

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
                type: categories[f.random.number({ min: 0, max: 2 })],
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
        return badges
            .filter((_, i) => i % 2 == 0)
            .map((x: Badge) => {
                const acquiredBadge: AcquiredBadge = {
                    badgeId: x.id,
                    dateAcquired: new Date()
                };
                return acquiredBadge;
            });
    }

    static getAllAvailableCategories(): string[] {
        return categories.slice()
    }
    static getAllAvailableTopics(): string[] {
        return topics.slice();
    }
}