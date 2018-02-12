import { IRecommendation } from "../interfaces/models";
import { apiFetch, apiPost } from "./APIRepository";

export default class RecommendationRepository {

    static findRecommendations(): Promise<IRecommendation[]> {
        return apiFetch<IRecommendation[]>("/recommendations/recommendations/find/all/");
    }

    static pendingRecommendations(): Promise<IRecommendation[]> {
        return apiFetch<IRecommendation[]>("/recommendations/recommendations/pending/all/");
    }

    static reviewRecommendations(): Promise<IRecommendation[]> {
        return apiFetch<IRecommendation[]>("/recommendations/recommendations/review/all/");
    }

    static updateUserStatus(id: number, status: string, location: string | undefined) {
        let data = location ? { id, status, location } : { id, status };
        return apiPost(`/recommendations/recommendations/find/update/`, data);
    }

    static updateReviewStatus(id: number, status: string) {
        let data = { id, status };
        return apiPost(`/recommendations/recommendations/review/update/`, data);
    }
}
