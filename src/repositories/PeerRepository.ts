import { Peer } from "../interfaces/models";
import f from "faker";

export default class PeerRepository {

    /**
     * Returns an array of Peer objects
     * @param {number} peerCount The number of peers to return
     * @return {Peer[]} An array of Peers with length peerCount
     */
    static getMany(peerCount: number): Peer[] {
        return new Array(peerCount).fill(0).map((_, i) => {
            const proficiencies = new Array(f.random.number({ min: 1, max: 4 }))
                .fill(0).map(x => f.hacker.abbreviation()) as string[];

            const availableTimes = new Array(f.random.number({ min: 1, max: 4 }))
                .fill(0).map((_, i) => {
                    const time = f.date.recent();
                    let hours = time.getHours() + 1;
                    if (hours == 12) {
                        return "12 PM";
                    } else if (hours < 12) {
                        return `${hours} AM`;
                    } else {
                        return `${(hours - 12)} PM`;
                    }
                });

            const peer: Peer = {
                id: f.random.number(),
                name: f.name.findName(),
                bio: f.hacker.phrase() + " " + f.hacker.phrase(),
                proficiencies: proficiencies,
                image: f.image.avatar(),
                availableTimes: availableTimes
            };

            return peer;
        });
    }
}