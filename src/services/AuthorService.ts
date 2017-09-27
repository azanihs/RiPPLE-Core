export default class AuthorService {

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

    static extractImagesFromDOM(body: string): { content: string, payload: string[] } {
        // Extracts the base64 strings from all image tags in the provided HTMLBodyElement
        // Assigns them ID's to identify image tags with their respective content
        // Returns this object representation ready for server upload
        return {
            content: "",
            payload: []
        };
    }
}
