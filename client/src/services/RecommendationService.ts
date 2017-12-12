import RecommendationRepository from "../repositories/RecommendationRepository";

export default class RecommendationService {

    static getFindRecommendations(): Promise<IRecommendation[]> {
        return RecommendationRepository.getFindRecommendations();
    }

    static getReviewRecommendations(): Promise<IRecommendation[]> {
        return RecommendationRepository.getReviewRecommendations();
    }
}
