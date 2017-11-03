export default class ImageService {
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
}
