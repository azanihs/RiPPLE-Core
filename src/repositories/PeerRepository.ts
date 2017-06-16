import { Peer } from "../interfaces/models";
import faker from "faker";

const f = faker as any;
export default class QuestionRepository {

    /**
     * Returns an array of Peer objects
     * @param peerCount The number of peers to return
     * @return Peer[]
     */
    static getMulti(peerCount: number): Peer[] {
        return new Array(peerCount).fill(0).map((_, i) => {
            const proficiencies = new Array(f.random.number({min: 1, max: 4}))
                .fill(0).map(x => f.hacker.abbreviation()) as string[];

            let availableTimes = new Array(f.random.number({min: 1, max: 4}))
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

            const peers: Peer = {
                id: f.random.number(),
                name: f.name.findName(),
                bio: f.hacker.phrase() + " " + f.hacker.phrase(),
                proficiencies: proficiencies,
                image: f.image.avatar(),
                availableTimes: availableTimes
            };

            return peers;
        });
    }
}