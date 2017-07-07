import { User, Peer } from "../interfaces/models";
import PeerRepository from "./PeerRepository";
import f from "faker";

const categories = ["Provide Mentorship", "Seek Mentorship", "Find Study Partner"];
const topics = new Array(10).fill(0).map(x => f.hacker.abbreviation()).filter((x, i, self) => self.indexOf(x) == i);
export default class UserRepository {

    /**
     * Returns an array of Peer objects
     * @param {number} peerCount The number of peers to return
     * @return {Peer[]} An array of Peers with length peerCount
     */
    static getLoggedInUser(): User {
        const peer: Peer = PeerRepository.getMany(1)[0];
        const connections = new Array(f.random.number({ min: 10, max: 100 })).fill(0).map(x => {
            const connection = {
                id: performance.now(),
                type: categories[f.random.number({ min: 0, max: 2 })],
                topic: topics[f.random.number({ min: 0, max: 10 })],
                weight: f.random.number({ min: 0, max: 10 })
            }
            return connection;
        });

        const user: User = {
            id: performance.now(),
            self: peer,
            connections: connections
        };

        return user;
    }

    static getAllAvailableCategories(): string[] {
        return categories.slice()
    }
    static getAllAvailableTopics(): string[] {
        return topics.slice();
    }
}