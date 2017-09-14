import Vue from "vue";
type PrimitiveMap = { [key: string]: number | string | boolean | number[] };
type FetcherIdentifer = string;
type FetcherFunctions<T> = (params?: PrimitiveMap) => Promise<T>;

let subscriptionCount = 0;

export default class Fetcher<T extends any> {
    private static functionIdentifiers: WeakMap<Function, string> = new WeakMap();
    private static functionParamMap: Map<FetcherIdentifer, Fetcher<any>> = new Map();

    private static sharedBus = new Vue();

    private readonly identifier: FetcherIdentifer;
    private readonly fn: Function;
    private readonly params: PrimitiveMap;

    static subscriptionLookup(subscription: Function) {
        if (Fetcher.functionIdentifiers.get(subscription) === undefined) {
            Fetcher.functionIdentifiers.set(subscription, `${subscription.name}_${subscriptionCount++}`);
        }
        return Fetcher.functionIdentifiers.get(subscription);
    }

    static serialize(fn: Function, params: PrimitiveMap): FetcherIdentifer {
        const functionIdentifier = Fetcher.subscriptionLookup(fn);
        const orderedParams = Object.keys(params).sort().map(x => [x, params[x]]);
        return `${functionIdentifier}_${JSON.stringify(orderedParams)}`;
    }

    static get<T extends any>(fn: FetcherFunctions<T>, params: PrimitiveMap = {}, policy?: number) {
        const serialisedIdentifier = Fetcher.serialize(fn, params);
        if (Fetcher.functionParamMap.get(serialisedIdentifier) === undefined) {
            const fetcherInstance = new Fetcher(serialisedIdentifier, fn, params);
            Fetcher.functionParamMap.set(serialisedIdentifier, fetcherInstance);
        }

        return Fetcher.functionParamMap.get(serialisedIdentifier);
    }

    private constructor(identifier: FetcherIdentifer, fn: FetcherFunctions<T>, params: PrimitiveMap) {
        this.identifier = identifier;
        this.fn = fn;
        this.params = { ...params }; // copy object
    }

    run() {
        this.fn(this.params)
            .then(x => {
                Fetcher.sharedBus.$emit(this.identifier, x);
            });
    }

    on = (callback: Function) => {
        Fetcher.sharedBus.$on(this.identifier, callback);
        this.run();
    };

    off = (callback: Function) => Fetcher.sharedBus.$off(this.identifier, callback);
}
