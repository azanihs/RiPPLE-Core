import "whatwg-fetch";
declare const process;
declare let fetch;

let token = undefined;

export const API = process.env.API_LOCATION;
export const NODE_ENV = process.env.NODE_ENV;

export const apiFetch = (url: string, opts?: Object) => {
    const headers = (opts || {})["headers"] || new Headers();
    if (token !== undefined) {
        headers.append("Authorization", token);
    };

    return fetch(`${API}${url}`, Object.assign(opts || {}, {
        headers: headers
    }))
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
