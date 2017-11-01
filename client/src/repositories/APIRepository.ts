import "whatwg-fetch";
declare const process;
declare let fetch;

let token = undefined;

export const API = process.env.API_LOCATION;
export const NODE_ENV = process.env.NODE_ENV;

const mergeAuthHeader = (options: Object) => {
    if (options === undefined) {
        options = {};
    }

    if (options["headers"] === undefined) {
        options["headers"] = new Headers();
    }

    if (token !== undefined) {
        options["headers"].append("Authorization", token);
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

export const apiFetch = (url: string, opts?: Object) => {
    const options = mergeAuthHeader(opts);

    return fetch(`${API}${url}`, options)
        .then(response => {
            if (!response.ok) {
                throw response;
            }
            return response;
        });
};

export const setToken = newToken => {
    token = newToken;
};
