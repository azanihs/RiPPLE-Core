import "whatwg-fetch";
import { IServerResponse } from "../interfaces/models";
import { addEventsToQueue, notificationToSnackbar } from "../util";

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
                    return Promise.resolve({}) as Promise<IServerResponse<T>>;
                } else {
                    return response.json() as Promise<IServerResponse<T>>;
                }
            }
            // Fallthrough to error
            return Promise.resolve({}) as Promise<IServerResponse<T>>;
        })
        .then(x => {
            if (x.notifications && x.notifications.length > 0) {
                for (let n of x.notifications) {
                    addEventsToQueue([notificationToSnackbar(n)]);
                }
            }

            if (x.error) {
                throw x.error;
            } else {
                return Promise.resolve(x.data);
            }
        })
        .catch((err: Response) => {
            if (typeof err.json !== "function") {
                throw err;
            } else {
                return err.json().then((errorObject: any) => {
                    if (errorObject.error) {
                        // TODO: Handle global things
                        addEventsToQueue([{
                            icon: "error",
                            name: `Server Error`,
                            description: `${errorObject.error}`
                        }]);
                    }
                    throw err;
                });
            }
        });
};

export const apiPost = <T>(url: string, body: Object, opts?: RequestInit) => {
    const postOptions = {
        method: "POST",
        headers: new Headers({
            "Accept": "application/json",
            "Content-Type": "application/json"
        }),
        body: JSON.stringify(body)
    };
    if (opts) {
        Object.assign(postOptions, opts);
    }

    return apiFetch<T>(url, postOptions);
};

export const setToken = (newToken: string) => {
    token = newToken;
};
