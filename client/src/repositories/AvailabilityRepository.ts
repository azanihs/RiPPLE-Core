import { IAvailability, ICourseAvailability, IDay, ITime, IAvailableRole, IStudyRole } from "../interfaces/models";
import { apiFetch } from "./APIRepository";

export default class AvailabilityRepository {

    static getUTCTimeSlots(): Promise<ITime[]> {
        return apiFetch<ITime[]>("/recommendations/availability/times/");
    }

    static getCourseAvailability(): Promise<ICourseAvailability[]> {
        return apiFetch<ICourseAvailability[]>("/recommendations/availability/all/");
    }

    static getDays(): Promise<IDay[]> {
        return apiFetch<IDay[]>("/recommendations/availability/days/");
    }

    static getUserAvailability(): Promise<IAvailability[]> {
        return apiFetch<IAvailability[]>("/recommendations/availability/");
    }

    static updateUserAvailability(day: number, time: number): Promise<IAvailability> {
        return apiFetch<IAvailability>(`/recommendations/availability/update/`, {
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

    static getStudyRoles(): Promise<IStudyRole[]> {
        return apiFetch<IStudyRole[]>("/recommendations/roles/all/");
    }

    static getUserAvailableRoles(): Promise<IAvailableRole[]> {
        return apiFetch<IAvailableRole[]>("/recommendations/roles/");
    }

    static updateUserRoles(topic: number, studyRole: number): Promise<IAvailableRole> {
        return apiFetch<IAvailableRole>(`/recommendations/roles/update/`, {
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
