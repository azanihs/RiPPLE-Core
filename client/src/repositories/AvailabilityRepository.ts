import { Availability, CourseAvailability, Day, Time, StudyRole, AvailableRole } from "../interfaces/models";
import { setToken, apiFetch } from "./APIRepository";

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
        });
    }

    static getStudyRoles(): Promise<StudyRole[]> {
        return apiFetch("/recommendations/roles/all");
    }

    static getUserAvailableRoles(): Promise<AvailableRole[]> {
        return apiFetch("/recommendations/roles/");
    }

    static updateUserRoles(topic: number, studyRole: number) {
        return apiFetch(`/recommendations/roles/update/`, {
            method: "POST",
            headers: new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json"
            }),
            body: JSON.stringify({
                topic: topic,
                studyRole: studyRole
            })
        });
    }
}
