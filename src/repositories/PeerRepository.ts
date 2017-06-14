import {Peer} from "../interfaces/models";
import faker from "faker";

const f = faker as any;
export default class QuestionRepository {
    /**
     * Returns a
     * @param peerCount The number of peers to return
     * @return Peer[]
     */

    static getMulti(peerCount:number):Peer[] {
        return new Array(peerCount).fill(0).map((_, i) => {
            let peerTitle = f.company.catchPhrase(); /* generate a random name here */
            let peerContent = f.hacker.phrase();

            const peers: Peer = {
                id: i,
                rating: f.random.number({min: 0, max: 200}),

                title: peerTitle,
                topic: f.hacker.abbreviation(),
                content: peerContent
            };
        return peers;
        });
    }
}