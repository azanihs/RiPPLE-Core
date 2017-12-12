import { IRecommendation } from "../interfaces/models";
import { apiFetch, apiPost } from "./APIRepository";

export default class RecommendationRepository {

    static getFindRecommendations(): Promise<IRecommendation[]> {
      return apiFetch<IRecommendation[]>("/recommendations/find/all/");
    }

    static getReviewRecommendations(): Promise<IRecommendation[]> {
      return apiFetch<IRecommendation[]>("/recommendations/review/all/");
    }
}
