import { Trait, Vue, Lifecycle } from "av-ts";
import ApplicationService from "./services/ApplicationService";

@Trait
export default class responsiveMobile extends Vue {

    mobileMode: boolean | undefined = false;

    @Lifecycle
    mounted() {
        this.$nextTick( function() {
            this.mobileMode = ApplicationService.getMobileMode();
        });
    }
}
