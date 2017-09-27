export default class AuthorService {

    static fileToBase64EncodeString(file: File): Promise<string> {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.addEventListener("loadend", () => {
                resolve(reader.result);
            });
        });
    }
}
