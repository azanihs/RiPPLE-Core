import { Topic, Edge, Course, CompareSet } from "../interfaces/models";
import UserRepository from "../repositories/UserRepository";
import TopicRepository from "../repositories/TopicRepository";

function addTopicsToEdgeList(topics: Topic[], edges: Edge[]) {
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
    static generateGraph(sourceData: Edge[], otherData: Edge[], exclude: number[]): CompareSet {
        const ownScores = sourceData;
        const userGoals = otherData;
        const topics = ownScores
            .map(x => x.source)
            .concat(ownScores.map(x => x.target))
            .reduce((carry: Topic[], topicNode: Topic) => {
                if (!carry.find(x => x == topicNode)) {
                    carry.push(topicNode);
                }
                return carry;
            }, [])
            .filter(x => !exclude.find(e => e === x.id));

        return {
            topics: topics, // Node List
            ownScores: ownScores, // Edge list of self
            compareAgainst: userGoals // Edge list of other
        };
    }

    static userCompetencies({ compareTo, exclude }: { compareTo: string, exclude?: undefined | number[] }) {
        const excludeTopics = exclude || [];
        return Promise.all([UserRepository.getUserCompetencies(), UserRepository.getCompareAgainst(compareTo)])
            .then(data => UserService.generateGraph(data[0], data[1], excludeTopics))
            .then(graph => TopicRepository.getAllAvailableTopics()
                .then(allTopics => allTopics.filter(x => !excludeTopics.find(e => e === x.id)))
                .then(topics => {
                    // Add in all self-loops
                    graph.topics = topics;
                    graph.ownScores = addTopicsToEdgeList(topics, graph.ownScores);
                    graph.compareAgainst = addTopicsToEdgeList(topics, graph.compareAgainst);
                    return graph;
                }));
    }

    static getEngagementScores({ compareTo, exclude }: { compareTo: string, exclude?: undefined | number[] }) {
        compareTo;

        return Promise.all([UserRepository.getUserEngagement(), UserRepository.getUserEngagement()])
            .then(data => UserService.generateGraph(data[0], data[1], exclude || []));
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

    static updateCourse(data: { course: Course, topics: Topic[] }) {
        return UserRepository.updateCourse(data.course, data.topics);
    }
}
