import { Availability, CourseAvailability, Time, StudyRole } from "../interfaces/models";
import { setToken, apiFetch } from "./APIRepository";

export default class AvailabilityRepository {

    static getUTCTimeSlots(): Promise<Time[]> {
        return apiFetch("/recommendations/availability/times")
            .then(x => x.json());
    }

    static getCourseAvailability(): Promise<CourseAvailability[]> {
        return apiFetch("/recommendations/availability/all")
            .then(x => x.json());
    }

    static getUserAvailability(): Promise<Availability[]> {
        return apiFetch("/recommendations/availability/")
            .then(x => x.json());
    }

    static updateUserAvailability(day: number, time: number) {
        return apiFetch(`/recommendations/availability/update/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                day: day,
                time: time
            })
        })
            .then(x => {
                return x.json();
            });
    }

    static getStudyRoles(): Promise<StudyRole[]> {
        return apiFetch("/recommendations/roles/all")
            .then(x => x.json());
    }
}
