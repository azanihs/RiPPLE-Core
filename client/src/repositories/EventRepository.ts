import { IEvent } from "../interfaces/models";
import { apiFetch, apiPost } from "./APIRepository";

export default class EventRepository {
    static getWeekEvents(): Promise<IEvent[]> {
        return apiFetch<IEvent[]>("/recommendations/recommendations/events/week/");
    }

    static cancelEvent(id: number) {
        const data = { id, status: "cancelled" };
        return apiPost(`/recommendations/recommendations/events/update/`, data);
    }
}
