import { QuestionUpload, AuthorResponse } from "../interfaces/models";

import { blobFetch } from "../repositories/APIRepository";

export default class AuthorService {

    static uploadContent(upload: QuestionUpload, updateFunction: (newProgress: number) => void) {
        let i = 0;
        setInterval(() => {
            if (i <= 100) {
                updateFunction(i++);
            }
        }, 100);
    }

    static fileToBase64EncodeString(file: File): Promise<Object> {
        return new Promise((resolve, reject) => {
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

    static extractImagesFromDOM(body: string): Promise<AuthorResponse> {
        // Extracts the base64 strings from all image tags in the provided HTMLBodyElement
        // Assigns them ID's to identify image tags with their respective content
        // Returns this object representation ready for server upload
        const parser = new DOMParser();
        const dom = parser.parseFromString(body, "text/html").querySelector("body");

        const images = Array.from(dom.querySelectorAll("img"));
        const payloads: { [id: number]: string } = {};

        return Promise.all(
            images.map((image, i) => new Promise((resolve, reject) => {
                const url = new URL(image.src);
                //if (url.hostname == "" || url.hostname == window.location.hostname) {
                if (url.protocol == "data:") {
                    // Is a base64 image already
                    payloads[i] = image.src;
                    image.src = "#:" + i;
                    resolve(payloads[i]);
                } else if (url.protocol == "blob:") {
                    // Is a createObjectURL()
                    console.log(url);
                    blobFetch(url.href)
                        .then(response => response.blob())
                        .then(AuthorService.fileToBase64EncodeString)
                        .then(file => {
                            payloads[i] = file.base64;
                            image.src = "#:" + i;
                            resolve(payloads[i]);
                        });
                }
                //}
            }))
        )
            .then(_ => ({
                content: dom.innerHTML,
                payloads: payloads
            }));
    }
}
