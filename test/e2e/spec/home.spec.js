const assert = require("assert");

module.exports = {
    "beforeEach": browser => {
        const devServer = browser.globals.devServerURL;
        browser
            .url(devServer)
            .waitForElementVisible("body")
            .resizeWindow(1920, 1080);
    },

    "Desktop Question Browser Tests": browser => {
        browser
            .waitForElementVisible(".sideNavContainer .navbarContainer", 100000)
            .assert.containsText(".sideNavContainer .navbarContainer ul li:nth-of-type(1)", "PROFILE")
            .assert.containsText(".sideNavContainer .navbarContainer ul li:nth-of-type(2)", "AUTHOR directions")
            .assert.containsText(".sideNavContainer .navbarContainer ul li:nth-of-type(3)", "ANSWER lightbulb_outline")
            .end();
    }
};
