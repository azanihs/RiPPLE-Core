import { IEvent, ITopic, IDayTime } from "../interfaces/models";

import { makeUser, _n } from "./UserRepository";
import TopicRepository from "./TopicRepository";

const makeEvents = (topics: ITopic[], count: number) => {
    const events: IEvent[] = Array.from({ length: count }, () => makeEvent(topics));
    return events;
};

const makeEvent = (topics: ITopic[]) => {
    // 1. Make an IUser
    const user = makeUser();

    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

    // 2. Make an IDayTime
    const getDay = (i: number) => {
        return days[i];
    };

    const makeDayTime = () => {
        const startHour = _n(24);
        const endHour = (startHour + 1) % 24;
        const dayTime: IDayTime = {
            day: {
                id: _n(10),
                day: getDay(_n(7))
            },
            time: {
                id: _n(10),
                start: {
                    time: `${startHour}:00`,
                    hour: startHour
                },
                end: {
                    time: `${endHour}:00`,
                    hour: endHour
                }
            }
        };
        return dayTime;
    };

    const dayTime: IDayTime = makeDayTime();

    const locations = ["Library", "Study Hall", "Tutor Room"];
    const location = locations[_n(locations.length)];

    const event: IEvent = {
        dayTime: dayTime,
        user: user,
        topics: topics,
        location: location
    };
    return event;
};


export default class EventRepository {
    static getWeekEvents(): Promise<IEvent[]> {
        return new Promise(resolve => {
            TopicRepository.getAllAvailableTopics().then(topics => {
                resolve(makeEvents(topics, 3));
            });
        });
    }
}
