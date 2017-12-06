import AvailabilityRepository from "../repositories/AvailabilityRepository";

export default class AvailabilityService {

    static getCourseAvailability() {
        return AvailabilityRepository.getCourseAvailability();
    }

    static getDays() {
        return AvailabilityRepository.getDays();
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

    static updateUserRoles(topic: number, studyRole: number) {
        return AvailabilityRepository.updateUserRoles(topic, studyRole);
    }
}
