import EventRepository from "../repositories/EventRepository";

export default class EventService {
    static getWeekEvents() {
        return EventRepository.getWeekEvents();
    }
}
