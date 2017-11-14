import { Availability } from "../interfaces/models";
import { setToken, apiFetch } from "./APIRepository";

export default class AvailabilityRepository {

    static getCourseAvailability(): Promise<Availability[]> {
        return apiFetch("/recommendations/availability/all")
          .then(x => x.json());
    }

    static getUserAvailability(): Promise<Availability[]> {
        return apiFetch("/recommendations/availability/")
          .then(x => x.json());
    }

}
