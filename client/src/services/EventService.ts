import EventRepository from "../repositories/EventRepository";

export default class EventService {
    static getWeekEvents() {
        return EventRepository.getWeekEvents();
    }

    static cancelEvent(id: number) {
        return EventRepository.cancelEvent(id);
    }
}
