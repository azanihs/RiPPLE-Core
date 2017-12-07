import { QuestionUpload, QuestionBuilder, Topic } from "../interfaces/models";

import ImageService from "./ImageService";
import QuestionRepository from "../repositories/QuestionRepository";

interface IValidate {
    message: string,
    args: any,
    validateFunction: (args: any) => boolean
};

export default class AuthorService {

    static uploadContent(upload: QuestionUpload) {
        return QuestionRepository.uploadQuestion(upload);
    }

    static prepareUpload(question: QuestionBuilder) {
        const upload: QuestionUpload = {
            question: undefined,
            explanation: undefined,
            responses: {
                A: undefined,
                B: undefined,
                C: undefined,
                D: undefined
            },
            topics: question.topics
        };

        const responseHelper = (index: "A" | "B" | "C" | "D") => {
            return ImageService.extractImagesFromDOM(question.responses[index]).then(response => {
                response.isCorrect = question.correctIndex === index;
                upload.responses[index] = response;
            });
        };

        return ImageService.extractImagesFromDOM(question.content)
            .then(questionContent => {
                upload.question = questionContent;
            })
            .then(() => ImageService.extractImagesFromDOM(question.explanation))
            .then(questionExplanation => {
                upload.explanation = questionExplanation;
            })
            .then(() => Promise.all(["A", "B", "C", "D"].map((index: any) => responseHelper(index))))
            .then(() => upload);
    }

    static validateQuestions(question: QuestionBuilder) {
        const validators: IValidate[] = [{
            message: "Question cannot be empty",
            validateFunction: ImageService.domIsNotEmpty,
            args: question.content
        }, {
            message: "Question must have between 1 and 4 topics",
            validateFunction: (topics: Topic[]) => topics.length >= 1 && topics.length <= 4,
            args: question.topics
        }, {
            message: "Question response 'A' cannot be empty",
            validateFunction: ImageService.domIsNotEmpty,
            args: question.responses.A
        }, {
            message: "Question response 'B' cannot be empty",
            validateFunction: ImageService.domIsNotEmpty,
            args: question.responses.B
        }, {
            message: "Question response 'C' cannot be empty",
            validateFunction: ImageService.domIsNotEmpty,
            args: question.responses.C
        }, {
            message: "Question response 'D' cannot be empty",
            validateFunction: ImageService.domIsNotEmpty,
            args: question.responses.D
        }, {
            message: "You must select which response is correct",
            validateFunction: (_: any) => question.correctIndex !== "",
            args: ""
        }, {
            message: "Question explanation cannot be empty",
            validateFunction: ImageService.domIsNotEmpty,
            args: question.explanation
        }];

        for (let i = 0; i < validators.length; ++i) {
            const entry = validators[i];
            if (entry.validateFunction(entry.args) === false) {
                return entry.message;
            }
        }
        return "";
    }
}
