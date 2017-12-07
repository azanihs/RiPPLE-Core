import { IAvailability, ICourseAvailability, IDay, ITime, IAvailableRole, IStudyRole } from "../interfaces/models";
import { apiFetch, apiPost } from "./APIRepository";

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
        return apiPost<IAvailability>(`/recommendations/availability/update/`, { day, time });
    }

    static getStudyRoles(): Promise<IStudyRole[]> {
        return apiFetch<IStudyRole[]>("/recommendations/roles/all/");
    }

    static getUserAvailableRoles(): Promise<IAvailableRole[]> {
        return apiFetch<IAvailableRole[]>("/recommendations/roles/");
    }

    static updateUserRoles(topic: number, studyRole: number): Promise<IAvailableRole> {
        return apiPost<IAvailableRole>(`/recommendations/roles/update/`, { topic, studyRole });
    }
}
