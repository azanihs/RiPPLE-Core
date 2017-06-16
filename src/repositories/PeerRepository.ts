import {Peer} from "../interfaces/models";
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
            let peerTitle = f.name.findName(); /* generate a random name here */
            let peerContent = f.hacker.phrase();

            const proficiencies = new Array(f.random.number({min: 1, max: 4})).fill(0).map(x => f.hacker.abbreviation()) as string[];
            const peers: Peer = {
                id: i,
                name: f.name.findName(),
                bio: f.hacker.phrase() + " " + f.hacker.phrase(),
                proficiencies: proficiencies,
                image: GetRandomProfileImage(),
                time: f.date.recent()
            };
        return peers;
        });
    }
}