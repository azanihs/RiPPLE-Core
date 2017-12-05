import { QuestionUpload, AuthorResponse, QuestionBuilder, Topic } from "../interfaces/models";

import { blobFetch } from "../repositories/APIRepository";
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

    static extractImagesFromDOM(body: string): Promise<AuthorResponse> {
        // Extracts the base64 strings from all image tags in the provided HTMLBodyElement
        // Assigns them ID's to identify image tags with their respective content
        // Returns this object representation ready for server upload
        const parser = new DOMParser();
        const dom = parser.parseFromString(body, "text/html").querySelector("body")!;

        const images = Array.from(dom.querySelectorAll("img"));
        const payloads: { [id: number]: string } = {};

        return Promise.all(images.map((image, i) => new Promise(resolve => {
            const url = new URL(image.src);
            if (url.hostname == "" || url.hostname == window.location.hostname) {
                if (url.protocol == "data:") {
                    // Is a base64 image already
                    payloads[i] = image.src;
                    image.src = "#:" + i;
                    resolve(payloads[i]);
                } else if (url.protocol == "blob:") {
                    // Is a createObjectURL()
                    blobFetch(url.href)
                        .then(response => response.blob() as Promise<File>)
                        .then(fileBlob => ImageService.fileToBase64EncodeString(fileBlob))
                        .then(file => {
                            payloads[i] = file.base64;
                            image.src = "#:" + i;
                            resolve(payloads[i]);
                        });
                }
            }
        }))).then(_ => ({
            content: dom.innerHTML,
            payloads: payloads,
            isCorrect: false
        }));
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
            return AuthorService.extractImagesFromDOM(question.responses[index]).then(response => {
                response.isCorrect = question.correctIndex === index;
                upload.responses[index] = response;
            });
        };

        return AuthorService.extractImagesFromDOM(question.content)
            .then(questionContent => {
                upload.question = questionContent;
            })
            .then(() => AuthorService.extractImagesFromDOM(question.explanation))
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

    static validateQuestions(question: QuestionBuilder) {
        const validators: IValidate[] = [{
            message: "Question cannot be empty",
            validateFunction: this.domIsNotEmpty,
            args: question.content
        }, {
            message: "Question must have between 1 and 4 topics",
            validateFunction: (topics: Topic[]) => topics.length >= 1 && topics.length <= 4,
            args: question.topics
        }, {
            message: "Question response 'A' cannot be empty",
            validateFunction: this.domIsNotEmpty,
            args: question.responses.A
        }, {
            message: "Question response 'B' cannot be empty",
            validateFunction: this.domIsNotEmpty,
            args: question.responses.B
        }, {
            message: "Question response 'C' cannot be empty",
            validateFunction: this.domIsNotEmpty,
            args: question.responses.C
        }, {
            message: "Question response 'D' cannot be empty",
            validateFunction: this.domIsNotEmpty,
            args: question.responses.D
        }, {
            message: "You must select which response is correct",
            validateFunction: (_: any) => question.correctIndex !== "",
            args: ""
        }, {
            message: "Question explanation cannot be empty",
            validateFunction: this.domIsNotEmpty,
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
