import Vue from "vue";
type PrimitiveMap = { [key: string]: number | string | boolean | number[] };
type FetcherIdentifer = string;
type FetcherFunctions<T> = (params: any) => Promise<T>;

let subscriptionCount = 0;


const cache: Map<FetcherIdentifer, {
    timestamp: number,
    value: undefined | any
}> = new Map();

export default class Fetcher<T extends any> {
    private static functionIdentifiers: WeakMap<Function, string> = new WeakMap();
    private static functionParamMap: Map<FetcherIdentifer, Fetcher<any>> = new Map();

    private static sharedBus = new Vue();

    private readonly identifier: FetcherIdentifer;
    private readonly fn: Function;
    private readonly params: PrimitiveMap;

    static forceUpdate(clearCache: boolean = true) {
        if (clearCache) {
            cache.clear();
        }
        // Cause a refresh of all async data by firing all functions on event bus
        Fetcher.functionParamMap.forEach((value, _key) => {
            value.run();
        });
    }

    static subscriptionLookup(subscription: Function) {
        if (Fetcher.functionIdentifiers.get(subscription) === undefined) {
            Fetcher.functionIdentifiers.set(subscription, `${subscription.name}_${subscriptionCount++}`);
        }
        return Fetcher.functionIdentifiers.get(subscription);
    }

    static serialize(fn: Function, params: PrimitiveMap = {}): FetcherIdentifer {
        const functionIdentifier = Fetcher.subscriptionLookup(fn);
        const orderedParams = Object.keys(params).sort().map(x => [x, params[x]]);
        return `${functionIdentifier}_${JSON.stringify(orderedParams)}`;
    }

    static get<T>(fn: FetcherFunctions<T>, params: PrimitiveMap = {}) {
        const serialisedIdentifier = Fetcher.serialize(fn, params);
        if (Fetcher.functionParamMap.get(serialisedIdentifier) === undefined) {
            const fetcherInstance = new Fetcher(serialisedIdentifier, fn, params);
            Fetcher.functionParamMap.set(serialisedIdentifier, fetcherInstance);
        }
        const found = Fetcher.functionParamMap.get(serialisedIdentifier);
        if (found === undefined) {
            throw new TypeError(`Could not find: ${serialisedIdentifier}`);
        }
        return found;
    }

    private constructor(identifier: FetcherIdentifer, fn: FetcherFunctions<T>, params: PrimitiveMap) {
        this.identifier = identifier;
        this.fn = fn;
        this.params = { ...params }; // copy object
    }

    run() {
        const hasRequestedBefore = cache.get(this.identifier);
        if (hasRequestedBefore !== undefined && (hasRequestedBefore.timestamp + 100000) > Date.now()) {
            if (hasRequestedBefore.value !== undefined) {
                Fetcher.sharedBus.$emit(this.identifier, hasRequestedBefore.value);
                return;
            }
            // Wait for in-flight request to complete
            return;
        }
        const cacheResult = {
            timestamp: Date.now(),
            value: undefined
        };
        cache.set(this.identifier, cacheResult);
        this.fn(this.params)
            .then((x: any) => {
                cacheResult.value = x;
                Fetcher.sharedBus.$emit(this.identifier, x);
            });
    }

    on = (callback: Function) => {
        Fetcher.sharedBus.$on(this.identifier, callback);
        this.run();
    };

    off = (callback: Function) => Fetcher.sharedBus.$off(this.identifier, callback);
}
