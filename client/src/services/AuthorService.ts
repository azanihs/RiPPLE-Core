import { QuestionUpload, AuthorResponse, QuestionBuilder } from "../interfaces/models";

import { blobFetch } from "../repositories/APIRepository";
import ImageService from "./ImageService";
import QuestionRepository from "../repositories/QuestionRepository";

export default class AuthorService {

    static uploadContent(upload: QuestionUpload) {
        return QuestionRepository.uploadQuestion(upload);
    }

    static extractImagesFromDOM(body: string): Promise<AuthorResponse> {
        // Extracts the base64 strings from all image tags in the provided HTMLBodyElement
        // Assigns them ID's to identify image tags with their respective content
        // Returns this object representation ready for server upload
        const parser = new DOMParser();
        const dom = parser.parseFromString(body, "text/html").querySelector("body");

        const images = Array.from(dom.querySelectorAll("img"));
        const payloads: { [id: number]: string } = {};

        return Promise.all(images.map((image, i) => new Promise((resolve, reject) => {
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
                        .then(response => response.blob())
                        .then(ImageService.fileToBase64EncodeString)
                        .then(file => {
                            payloads[i] = file.base64;
                            image.src = "#:" + i;
                            resolve(payloads[i]);
                        });
                }
            }
        }))).then(_ => ({
            content: dom.outerHTML,
            payloads: payloads
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

        const responseHelper = index => AuthorService.extractImagesFromDOM(question.responses[index])
            .then(response => {
                upload.responses[index] = response;
                upload.responses[index].isCorrect = question.correctIndex === index;
            });

        return AuthorService.extractImagesFromDOM(question.content)
            .then(questionContent => {
                upload.question = questionContent;
            })
            .then(() => AuthorService.extractImagesFromDOM(question.explanation))
            .then(questionExplanation => {
                upload.explanation = questionExplanation;
            })
            .then(() => Promise.all(["A", "B", "C", "D"].map(responseHelper)))
            .then(() => upload);
    }

    static domIsNotEmpty(questionDOM) {
        const getBody = (html: string) => {
            const domParser = new DOMParser();
            const questionDOM = domParser.parseFromString(html, "text/html");
            return questionDOM.querySelector("body").outerHTML.trim();
        };

        const questionBody = getBody(questionDOM);
        return questionBody.length > 0;
    }

    static validateQuestions(question: QuestionBuilder) {
        const validator = {
            "Question cannot be empty": {
                validateFunction: this.domIsNotEmpty,
                args: question.content
            },
            "Question must have between 1 and 4 topics": {
                validateFunction: topics => topics.length >= 1 && topics.length <= 4,
                args: question.topics
            },
            "Question response 'A' cannot be empty": {
                validateFunction: this.domIsNotEmpty,
                args: question.responses.A
            },
            "Question response 'B' cannot be empty": {
                validateFunction: this.domIsNotEmpty,
                args: question.responses.B
            },
            "Question response 'C' cannot be empty": {
                validateFunction: this.domIsNotEmpty,
                args: question.responses.C
            },
            "Question response 'D' cannot be empty": {
                validateFunction: this.domIsNotEmpty,
                args: question.responses.D
            },
            "You must select which question is correct": {
                validateFunction: x => question.correctIndex !== "",
                args: ""
            },
            "Question explanation cannot be empty": {
                validateFunction: this.domIsNotEmpty,
                args: question.explanation
            }
        };

        for (let errorMessage in validator) {
            if (validator[errorMessage] !== undefined) {
                const args = validator[errorMessage].args;
                if (validator[errorMessage].validateFunction(args) === false) {
                    return errorMessage;
                }
            }
        }
        return "";
    }
}
