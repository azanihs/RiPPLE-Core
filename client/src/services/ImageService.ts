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
}
