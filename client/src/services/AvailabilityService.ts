import { Availability, Day, Time, StudyRole } from "../interfaces/models";
import AvailabilityRepository from "../repositories/AvailabilityRepository";

export default class AvailabilityService {

    static getCourseAvailability() {
        return AvailabilityRepository.getCourseAvailability();
    }

    static getUserAvailability() {
        return AvailabilityRepository.getUserAvailability();
    }

    static updateUserAvailability(day: number, time: number) {
        return AvailabilityRepository.updateUserAvailability(day, time);
    }

    static getUTCTimeSlots() {
        return AvailabilityRepository.getUTCTimeSlots();
    }

    static getStudyRoles() {
        return AvailabilityRepository.getStudyRoles();
    }

    static getUserAvailableRoles() {
        return AvailabilityRepository.getUserAvailableRoles();
    }
}
