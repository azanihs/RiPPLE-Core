import { Vue, Trait } from "av-ts";

@Trait
class PropUpdate extends Vue {
    updateProp(propName: string) {
        return newValue => {
            this[propName] = newValue;
        };
    }
}

export default PropUpdate;
