import { IRecommendation } from "../interfaces/models";
import { apiFetch } from "./APIRepository";

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
}
