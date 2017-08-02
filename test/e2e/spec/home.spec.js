const assert = require("assert");

module.exports = {
    "Desktop Question Browser Tests": browser => {
        // automatically uses dev Server port from /config.index.js
        // default: http://localhost:8080
        // see nightwatch.conf.js
        const devServer = browser.globals.devServerURL;

        browser
            .resizeWindow(1920, 1080)
            .url(devServer)
            .waitForElementVisible(".sideNavContainer .navbarContainer", 100000)
            .assert.containsText(".sideNavContainer .navbarContainer ul li:nth-of-type(1)", "PROFILE")
            .assert.containsText(".sideNavContainer .navbarContainer ul li:nth-of-type(2)", "VIEW QUESTIONS")
            .assert.containsText(".sideNavContainer .navbarContainer ul li:nth-of-type(3)", "CONNECT TO PEERS")
            .click(".sideNavContainer .navbarContainer ul li:nth-of-type(2) a")
            .waitForElementVisible(".pageContent .headingContainer", 100000)
            .assert.elementPresent(".pageContent .headingContainer + div > div:nth-child(25)")
            .assert.elementNotPresent(".pageContent .headingContainer + div > div:nth-child(26)")
            .end();
    }
};
