import { eventBus, CacheMap, CacheLog, makeEmptyCache, subscriptionLookup } from "./Notify";


export default class CacheService {
    protected static caches: CacheMap = new Map();

    static subscribe(subscription: Function, param: any, callback: Function, force = true) {
        if (this.caches.get(subscription) === undefined) {
            this.caches.set(subscription, makeEmptyCache());

            const subscriptionQueue = this.caches.get(subscription).queue;
            const subscriptionName = subscriptionLookup(subscription);

            eventBus.$on(subscriptionName, dataGenerator => {
                subscriptionQueue.forEach(x => {
                    x.callback(dataGenerator(x.param));
                });
            });
        }

        this.caches.get(subscription).queue.push({
            param, callback
        });

        if (force === true) {
            subscription();
        }
    }

    static emit(subscription: Function, emitFn: Function) {
        const subscriptionName = subscriptionLookup(subscription);
        eventBus.$emit(subscriptionName, emitFn);
    }

    static getCache(subscription: Function): CacheLog {
        return this.caches.get(subscription);
    }
}
