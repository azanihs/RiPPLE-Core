import { IQuestionUpload, IQuestionBuilder, ITopic } from "../interfaces/models";

import ImageService from "./ImageService";
import QuestionRepository from "../repositories/QuestionRepository";

interface IValidate {
    message: string,
    args: any,
    validateFunction: (args: any) => boolean
};

export default class AuthorService {

    static uploadContent(upload: IQuestionUpload, path: string) {
        return QuestionRepository.uploadQuestion(upload, path);
    }

    static prepareUpload(question: IQuestionBuilder) {
        const upload: IQuestionUpload = {
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

    static domIsNotEmpty(questionDOMString: string) {
        const getBody = (html: string) => {
            const domParser = new DOMParser();
            const questionDOM = domParser.parseFromString(html, "text/html");
            return questionDOM.querySelector("body")!.innerHTML.trim();
        };

        const questionBody = getBody(questionDOMString);
        return questionBody.length > 0;
    }

    static validateQuestions(question: IQuestionBuilder) {
        const validators: IValidate[] = [{
            message: "Question cannot be empty",
            validateFunction: ImageService.domIsNotEmpty,
            args: question.content
        }, {
            message: "Question must have between 1 and 4 topics",
            validateFunction: (topics: ITopic[]) => topics.length >= 1 && topics.length <= 4,
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
