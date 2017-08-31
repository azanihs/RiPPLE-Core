import { Vue, Trait } from "av-ts";

@Trait
class PropUpdate extends Vue {
    propUpdate(propName: string) {
        return (newValue: any) => {
            this[propName] = newValue;
        }
    }
}

export default PropUpdate;