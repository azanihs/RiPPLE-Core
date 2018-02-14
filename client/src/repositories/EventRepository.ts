import { IEvent } from "../interfaces/models";
import { apiFetch } from "./APIRepository";

export default class EventRepository {
    static getWeekEvents(): Promise<IEvent[]> {
        return apiFetch<IEvent[]>("/recommendations/recommendations/events/week/");
    }
}
