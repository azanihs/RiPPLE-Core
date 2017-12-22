import { Trait, Vue, Lifecycle } from "av-ts";
import ApplicationService from "./services/ApplicationService";
import Fetcher from "./services/Fetcher";

@Trait
export default class responsiveMobile extends Vue {

    mobileMode: boolean = false;

    updateMobileMode(newMode: boolean) {
        this.mobileMode = newMode;
    }

    @Lifecycle
    created() {
        Fetcher.get(ApplicationService.getMobileMode)
            .on(this.updateMobileMode);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(ApplicationService.getMobileMode)
            .off(this.updateMobileMode);
    }
}
