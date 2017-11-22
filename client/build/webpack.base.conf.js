var fs = require("fs");
const path = require('path');
//var config = require('../config');
// var utils = require('./utils');
var projectRoot = path.resolve(__dirname, '../');
var webpack = require('webpack');
var ExtractTextPlugin = require("extract-text-webpack-plugin");

var env = process.env.NODE_ENV
// check env & config/index.js to decide weither to enable CSS Sourcemaps for the
// various preprocessor loaders added to vue-loader at the end of this file
var cssSourceMapDev = false; // (env === 'development' && config.dev.cssSourceMap)
var cssSourceMapProd = false // (env === 'production' && config.build.productionSourceMap)
var useCssSourceMap = cssSourceMapDev || cssSourceMapProd

function placeDefaults(fileName) {
    var exists = fs.existsSync(fileName);
    if (!exists) {
        console.warn("Writing default env settings to: " + fileName);
        fs.writeFileSync(fileName, "NODE_ENV=development\nAPI_LOCATION=http://localhost:8000");
    }
}

if (env == "development") {
    placeDefaults("./.env.dev");
} else if (env == "production") {
    placeDefaults("./.env.prod");
} else {
    throw new Error("No environment detected")
}

module.exports = {
    entry: {
        app: [
            './src/main.ts'
        ]
    },
    output: {
        path: path.resolve(__dirname, "../dist"),
        publicPath: process.env.NODE_ENV === 'production' ? "./" : "/",
        filename: './[name].[hash].js'
    },
    resolve: {
        extensions: ['.js', '.vue', '.ts', '.css'],
        alias: {
            'vue$': 'vue/dist/vue.common.js',
            '@': path.resolve(__dirname, '../src'),
            'assets': path.resolve(__dirname, '../src/assets'),
            'components': path.resolve(__dirname, '../src/components')
        },
        modules: ["node_modules", "lib", "style"]
    },
    module: {
        rules: [{
                enforce: "pre",
                test: /.vue$/,
                loader: "eslint-loader",
                exclude: "/node_modules/"
            }, {
                enforce: "pre",
                test: /.ts$/,
                loader: "eslint-loader",
                exclude: "/node_modules/"
            }, {
                test: /\.ts$/,
                loader: 'ts-loader',
                options: {
                    appendTsSuffixTo: [/\.vue$/],
                    silent: true
                },
                include: [path.resolve(__dirname, "../"), path.resolve(__dirname, "../typings/modules")],
                exclude: /node_modules/
            }, {
                test: /\.json$/,
                loader: 'json-loader'
            }, {
                test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
                loader: 'url-loader',
                query: {
                    limit: 10000,
                    name: 'img/[name].[hash:7].[ext]'
                }
            }, {
                test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
                loader: 'url-loader',
                query: {
                    limit: 10000,
                    name: 'fonts/[name].[hash:7].[ext]'
                }
            }

        ]
    }
}
