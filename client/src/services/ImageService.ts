import { blobFetch } from "../repositories/APIRepository";
import { AuthorResponse } from "../interfaces/models";

interface ConvertedFile {
    file: string,
    base64: string,
    _meta: {
        src: string,
        alt: string,
        text: string,
        title: string
    }
}
export default class ImageService {
    static fileToBase64EncodeString(file: File): Promise<ConvertedFile> {
        return new Promise(resolve => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.addEventListener("loadend", () => {
                resolve({
                    file: file.name,
                    base64: reader.result,
                    _meta: {
                        src: URL.createObjectURL(file),
                        alt: file.name,
                        text: file.name,
                        title: file.name
                    }
                });
            });
        });
    }

    static handleFileClick(resolve: any, _currentFieldValue: any, fieldMeta: any) {
        if (fieldMeta.filetype != "image") {
            return;
        }

        const input = document.createElement("input")!;
        input.type = "file";

        input.addEventListener("change", () => {
            const inputFiles = input.files!;
            if (inputFiles.length != 1) {
                return;
            }
            const file = inputFiles[0];
            ImageService.fileToBase64EncodeString(file)
                .then(x => {
                    // * tinyMCE will encode the uploaded image with an window.createObjectURL until it loses focus.
                    // ** It will use the base64 encoding when focus is lost.
                    // * When upload time happens, just pull all img srcs from the DOM object, and if they are not a base64 then encode the object to be so
                    resolve(x.base64, x._meta);
                })
                .catch(err => {
                    console.warn(err);
                });
        });

        // Dispatch a click event
        const clickEvent = new MouseEvent("click", {
            "view": window,
            "bubbles": true,
            "cancelable": true
        });
        input.dispatchEvent(clickEvent);
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
                } else {
                    resolve(image.src);
                }
            } else {
                resolve(image.src);
            }
        }))).then(_ => {
            return {
                content: dom.innerHTML,
                payloads: payloads,
                isCorrect: false
            };
        });
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
}
