// This is a karma config file. For more details see
//   http://karma-runner.github.io/0.13/config/configuration-file.html
// we are also using it with karma-webpack
//   https://github.com/webpack/karma-webpack
process.env.NODE_ENV = "development"
const webpackConfig = require("../../build/webpack.dev.conf");
const path = require("path");

module.exports = config => {
    config.set({
        // to run in additional browsers:
        // 1. install corresponding karma launcher
        //    http://karma-runner.github.io/0.13/config/browsers.html
        // 2. add it to the `browsers` array below.
        browsers: ["PhantomJS"],
        frameworks: ["phantomjs-shim", "mocha", "chai"],
        reporters: ["spec", "coverage-istanbul"],
        files: ["../../node_modules/babel-polyfill/dist/polyfill.min.js", "spec/**/*.ts"],
        preprocessors: {
            "spec/**/*.ts": ["webpack"]
        },
        webpack: webpackConfig,
        webpackMiddleware: {
            noInfo: true
        },
        singleRun: true,
        coverageIstanbulReporter: {
            "reports": ["html", "text-summary"],
            // base output directory. If you include %browser% in the path it will be replaced with the karma browser name
            "dir": path.join(__dirname, "./coverage"),
            // if using webpack and pre-loaders, work around webpack breaking the source path
            "fixWebpackSourcePaths": true,
            "report-config": {
                // all options available at: https://github.com/istanbuljs/istanbul-reports/blob/590e6b0089f67b723a1fdf57bc7ccc080ff189d7/lib/html/index.js#L135-L137
                html: {
                    // outputs the report in ./coverage/html
                    subdir: "html"
                }
            }
        }
    });
};
