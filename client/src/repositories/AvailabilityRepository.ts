import { Availability, CourseAvailability, Day, Time, AvailableRole, StudyRole } from "../interfaces/models";
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

    static updateUserAvailability(day: number, time: number): Promise<Availability> {
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

    static getStudyRoles(): Promise<StudyRole[]> {
        return apiFetch<StudyRole[]>("/recommendations/roles/all");
    }

    static getUserAvailableRoles(): Promise<AvailableRole[]> {
        return apiFetch<AvailableRole[]>("/recommendations/roles/");
    }

    static updateUserRoles(topic: number, studyRole: number): Promise<AvailableRole> {
        return apiFetch<AvailableRole>(`/recommendations/roles/update/`, {
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
