import f from "faker";

const peers = new Array(100).fill(0).map((_, i) => {
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

    const peer = {
        id: f.random.number(),
        name: f.name.findName(),
        bio: f.hacker.phrase() + " " + f.hacker.phrase(),
        proficiencies: proficiencies,
        image: f.image.avatar(),
        availableTimes: availableTimes
    };

    return peer;
});

export default class PeerRepository {
    /*static getMany(peerCount: number): Promise<Peer[]> {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(peers.slice(0, peerCount));
            }, Math.random() * 1000);
        });
    }*/
}
