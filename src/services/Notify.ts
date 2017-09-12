import Vue from "vue";

let subscriptionCount = 0;

const caches: WeakMap<Function, string> = new WeakMap();

type CacheMap = WeakMap<Function, Object[]>;

const makeEmptyCache = () => {
    return [];
};

const subscriptionLookup = (subscription: Function) => {
    if (caches.get(subscription) === undefined) {
        caches.set(subscription, `${subscription.name}_${subscriptionCount++}`);
    }

    return caches.get(subscription);
};

const eventBus = new Vue();

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

const mergeStringCache = cache => x => {
    if (cache.find(c => c === x) === undefined) {
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
    CacheMap,

    makeEmptyCache,
    subscriptionLookup,

    mergeCache,
    mergeStringCache,
    every,
    eventBus
};
