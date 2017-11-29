import { Badge } from "../interfaces/models";
import { apiFetch } from "./APIRepository";

export default class BadgeRepository {

    static getAllUserBadges(): Promise<Badge[]> {
        return apiFetch<Badge[]>("/users/achievements/progress/");
    }
}
