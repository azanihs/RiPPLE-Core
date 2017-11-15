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
                return x.json()
                    .catch(_ => x);
            });
    }
}
