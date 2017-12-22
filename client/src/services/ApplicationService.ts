
let _isMobileMode: boolean = false;

import Fetcher from "./Fetcher";


export default class ApplicationService {

    static getMobileMode() {
        // return _isMobileMode;
        return Promise.resolve(_isMobileMode);
    }

    static setMobileMode(isMobile: boolean) {
        _isMobileMode = isMobile;
        Fetcher.get(ApplicationService.getMobileMode)
            .update(_isMobileMode);
    }
}
