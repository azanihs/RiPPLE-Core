import { ITopic, IEdge, ICourse, ICompareSet, IConsentForm } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";
import TopicRepository from "../repositories/TopicRepository";
import ImageService from "./ImageService";

interface IValidate {
    message: string,
    args: any,
    validateFunction: (args: any) => boolean
};

function addTopicsToEdgeList(topics: ITopic[], edges: IEdge[]) {
    topics.forEach(topic => {
        if (!edges.find(ownScore => ownScore.source == topic && ownScore.target == topic)) {
            edges = edges.concat({
                source: topic,
                target: topic,
                competency: 0,
                attempts: 0
            });
        }
    });
    return edges;
}

export default class UserService {
    static sendConsent(response: boolean) {
        return UserRepository.sendConsent(response);
    }

    static validateConsentForm(consentForm: IConsentForm) {
        const validators: IValidate[] = [{
            message: "Consent text cannot be empty",
            validateFunction: ImageService.domIsNotEmpty,
            args: consentForm.text
        }];
        for (let i = 0; i < validators.length; ++i) {
            const entry = validators[i];
            if (entry.validateFunction(entry.args) === false) {
                return entry.message;
            }
        }
        return "";
    }

    static prepareConsentUpload(consentForm: IConsentForm) {
        const upload: IConsentForm = {
            text: "undefined",
            author: consentForm.author
        };

        return ImageService.extractImagesFromDOM(consentForm.text)
            .then(consentContent => {
                upload.text = consentContent.content;
            }).then(() => upload);
    }

    static uploadContent(upload: IConsentForm) {
        return UserRepository.uploadConsentForm(upload);
    }


    static generateGraph(sourceData: IEdge[], otherData: IEdge[], exclude: number[]): ICompareSet {
        const ownScores = sourceData;
        const userGoals = otherData;
        const topics = ownScores
            .map(x => x.source)
            .concat(ownScores.map(x => x.target))
            .reduce((carry: ITopic[], topicNode: ITopic) => {
                if (!carry.find(x => x == topicNode)) {
                    carry.push(topicNode);
                }
                return carry;
            }, [])
            .filter(x => exclude.findIndex(e => e === x.id) === -1);

        return {
            topics: topics, // Node List
            ownScores: ownScores, // IEdge list of self
            compareAgainst: userGoals // IEdge list of other
        };
    }

    static userCompetencies({ compareTo, exclude }: { compareTo: string, exclude?: undefined | number[] }) {
        const excludeTopics = exclude || [];
        return Promise.all([UserRepository.getUserCompetencies(), UserRepository.getCompareAgainst(compareTo)])
            .then(data => UserService.generateGraph(data[0], data[1], excludeTopics))
            .then(graph => TopicRepository.getAllAvailableTopics()
                .then(allTopics => allTopics.filter(x => excludeTopics.findIndex(e => e === x.id) === -1))
                .then(topics => {
                    // Add in all self-loops
                    graph.topics = topics;
                    graph.ownScores = addTopicsToEdgeList(topics, graph.ownScores);
                    graph.compareAgainst = addTopicsToEdgeList(topics, graph.compareAgainst);
                    return graph;
                }));
    }

    static getEngagementScores({ compareTo, exclude }: { compareTo: string, exclude?: undefined | number[] }) {
        const excludeTopics = exclude || [];
        return Promise.all([UserRepository.getUserEngagement(), UserRepository.getEngagementAgainst(compareTo)])
            .then(data => UserService.generateGraph(data[0], data[1], excludeTopics));
    }

    static getAllAvailableEngagementTypes() {
        return UserRepository.getAllAvailableEngagementTypes();
    }

    static getUserPeers({ count }: { count: number }) {
        return UserRepository.getUserConnections(count);
    }

    static getEngagementSummary() {
        return UserRepository.getUserEngagement()
            .then(edges => edges.filter(x => x.target == x.source)
                .map(x => ({
                    node: x.target,
                    score: x.competency
                })));
    }

    static getLoggedInUser() {
        return UserRepository.getLoggedInUser();
    }

    static getConsentForm() {
        return UserRepository.getConsentForm();
    }

    static getAllAvailableCategories() {
        return UserRepository.getAllAvailableCategories();
    }

    static getRecommendedConnections({ count }: { count: number }) {
        return UserRepository.getUserConnections(count);
    }

    static getOutstandingRequests({ count }: { count: number }) {
        return UserRepository.getUserConnections(count);
    }

    static updateUserImage({ newImage }: { newImage: string }) {
        return UserRepository.updateUserImage(newImage);
    }

    static getMostReputableUsers({ sortField, sortOrder }: { sortField: string, sortOrder: "DESC" | "ASC" }) {
        return UserRepository.getUserLeaderboard(sortField, sortOrder);
    }

    static getUserNotifications() {
        return UserRepository.getUserNotifications();
    }

    static getMeetingHistory() {
        return UserRepository.getMeetingHistory();
    }

    static getUserCourses() {
        return UserRepository.getUserCourses();
    }

    static updateCourse(data: { course: ICourse, topics: ITopic[] }) {
        return UserRepository.updateCourse(data.course, data.topics);
    }
}
