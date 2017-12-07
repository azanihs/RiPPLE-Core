import "whatwg-fetch";
import { IServerResponse } from "../interfaces/models";
import { addEventsToQueue } from "../util";

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
                addEventsToQueue(x.notifications);
            }

            if (x.error) {
                // TODO: Handle global things
                addEventsToQueue([{
                    id: performance.now(),
                    icon: "error",
                    name: `Server Error`,
                    description: `${x.error}`
                }]);
                return Promise.resolve({}) as Promise<T>;
            } else {
                return Promise.resolve(x.data);
            }
        })
        .catch((err: Response) => err.json().then((errorObject: any) => {
            if (errorObject.error) {
                // TODO: Handle global things
                addEventsToQueue([{
                    id: performance.now(),
                    icon: "error",
                    name: `Server Error`,
                    description: `${errorObject.error}`
                }]);
            }
            throw err;
        }));
};

export const setToken = (newToken: string) => {
    token = newToken;
};
