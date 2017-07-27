const assert = require("assert");

module.exports = {
    "default e2e tests": function (browser) {
        // automatically uses dev Server port from /config.index.js
        // default: http://localhost:8080
        // see nightwatch.conf.js
        const devServer = browser.globals.devServerURL;

        browser
            .url(devServer)
            .waitForElementVisible(".navbarContainer", 1000)
            .assert.containsText(".navbarContainer ul li:nth-of-type(1)", "PROFILE")
            .assert.containsText(".navbarContainer ul li:nth-of-type(2)", "VIEW QUESTIONS")
            .assert.containsText(".navbarContainer ul li:nth-of-type(3)", "CONNECT TO PEERS")
            .click(".navbarContainer ul li:nth-of-type(2) a")
            .waitForElementVisible(".headingContainer", 10000)
            .assert.elementPresent(".headingContainer + div > div:nth-child(25)")
            .assert.elementNotPresent(".headingContainer + div > div:nth-child(26)")
            .end();
    }
};
