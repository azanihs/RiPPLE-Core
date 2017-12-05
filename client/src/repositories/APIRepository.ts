import "whatwg-fetch";

let token: undefined | string = undefined;

export const API = process.env.API_LOCATION;
export const NODE_ENV = process.env.NODE_ENV;

const mergeAuthHeader = (options?: RequestInit) => {
    if (options === undefined) {
        options = {
            headers: new Headers()
        };
    }

    if (!(options.headers instanceof Headers)) {
        console.warn(options.headers);
        throw new Error("Invalid header type");
    }

    if (options.headers === undefined) {
        options.headers = new Headers();
    }


    if (token !== undefined) {
        options.headers.append("Authorization", token);
    };

    return options;
};

export const blobFetch = (url: string, options?: Object) => {
    return fetch(`${url}`, options)
        .then(response => {
            if (!response.ok) {
                throw response;
            }
            return response;
        });
};

export const apiFetch = <T>(url: string, opts?: RequestInit): Promise<T> => {
    const options = mergeAuthHeader(opts);
    return fetch(`${API}${url}`, options)
        .then(response => {
            if (!response.ok) {
                throw response;
            }
            if (response.status >= 200 && response.status < 300) {
                if (response.status == 204) {
                    return Promise.resolve({}) as Promise<T>;
                } else {
                    return response.json() as Promise<T>;
                }
            }
            // Fallthrough to error
            return Promise.resolve({}) as Promise<T>;
        });
};

export const setToken = (newToken: string) => {
    token = newToken;
};
