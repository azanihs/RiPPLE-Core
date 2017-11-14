import { Availability, Day, Time } from "../interfaces/models";
import AvailabilityRepository from "../repositories/AvailabilityRepository";

export default class AvailabilityService {


    static getCourseAvailability() {
        return AvailabilityRepository.getCourseAvailability();
    }

    static getUserAvailability() {
        return AvailabilityRepository.getUserAvailability();
    }

}
