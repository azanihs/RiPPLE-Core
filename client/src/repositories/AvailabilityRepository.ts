import { Availability, CourseAvailability, Day, Time } from "../interfaces/models";
import { apiFetch } from "./APIRepository";

export default class AvailabilityRepository {

    static getUTCTimeSlots(): Promise<Time[]> {
        return apiFetch<Time[]>("/recommendations/availability/times/");
    }

    static getCourseAvailability(): Promise<CourseAvailability[]> {
        return apiFetch<CourseAvailability[]>("/recommendations/availability/all/");
    }

    static getDays(): Promise<Day[]> {
        return apiFetch<Day[]>("/recommendations/availability/days/");
    }

    static getUserAvailability(): Promise<Availability[]> {
        return apiFetch<Availability[]>("/recommendations/availability/");
    }


    static updateUserAvailability(day: number, time: number) {
        return apiFetch<Availability>(`/recommendations/availability/update/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                day: day,
                time: time
            })
        });
    }
}
