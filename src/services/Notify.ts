import Vue from "vue";

let subscriptionCount = 0;

const caches: Map<Function, string> = new Map();

type CacheLog = {
    queue: {
        param: any,
        callback: Function
    }[],
    cache: any[]
};
type CacheMap = Map<Function, CacheLog>;

const makeEmptyCache = () => {
    return {
        queue: [],
        cache: []
    };
};

const subscriptionLookup = (subscription: Function) => {
    if (caches.get(subscription) === undefined) {
        caches.set(subscription, `${subscriptionCount++}_cacheEvent`);
    }

    return caches.get(subscription);
};

const eventBus = new Vue();

const pushNotify = (notify: Function, data: any) => {
    if (typeof notify === "function") {
        notify(data);
    }
};

/**
 * @return <Boolean> True iff mutation happened
 */
const mergeCache = cache => x => {
    if (cache.find(c => c.id === x.id) === undefined) {
        cache.push(x);
        return true;
    }
    return false;
};

const every = forEach => cb => {
    let mutated = false;
    forEach.forEach(x => {
        if (cb(x) === true) {
            mutated = true;
        }
    });
    return mutated;
};


export {
    CacheLog,
    CacheMap,

    makeEmptyCache,
    subscriptionLookup,

    pushNotify,
    mergeCache,
    every,
    eventBus
};
