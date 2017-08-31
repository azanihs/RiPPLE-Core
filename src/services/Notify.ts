import Vue from "vue";

const eventBus = new Vue();


const pushNotify = (notify: Function, data: any) => {
    if (typeof notify === "function") {
        notify(data);
    }
};

const mergeCache = cache => x => {
    if (cache.find(c => c.id === x.id) === undefined) {
        cache.push(x);
    }
};

const mergeStringCache = cache => x => {
    if (cache.find(c => c === x) === undefined) {
        cache.push(x);
    }
};


export {
    pushNotify,
    mergeCache,
    mergeStringCache,
    eventBus
};
