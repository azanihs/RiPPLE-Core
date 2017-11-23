import { Vue } from "av-ts";
import VueRouter from "vue-router";

const router = new VueRouter({
    mode: "history",
    routes: []
});

export function makeComponent<T extends Vue>(Comp: any): T {
    return new Comp({
        router
    }) as T;
}
