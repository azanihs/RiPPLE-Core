import { IBadge } from "../interfaces/models";
import { apiFetch } from "./APIRepository";

export default class BadgeRepository {

    static getAllUserBadges(): Promise<IBadge[]> {
        return apiFetch<IBadge[]>("/users/achievements/progress/");
    }
}
