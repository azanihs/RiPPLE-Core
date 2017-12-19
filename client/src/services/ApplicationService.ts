
let _isMobileMode: boolean = false;

export default class ApplicationService {
    static getMobileMode() {
        return _isMobileMode;
    }

    static setMobileMode(isMobile: boolean) {
        _isMobileMode = isMobile;
    }
}
