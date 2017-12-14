const path = require("path")
const webpack = require("webpack")
const merge = require("webpack-merge")
const baseWebpackConfig = require("./webpack.base.conf")
const ExtractTextPlugin = require("extract-text-webpack-plugin")
const HtmlWebpackPlugin = require("html-webpack-plugin")
const Dotenv = require("dotenv-webpack");

var webpackConfig = merge(baseWebpackConfig, {
    devtool: "#source-map",
    output: {
        path: path.resolve(__dirname, '../dist'),
        filename: "static/js/[name].[chunkhash].js",
        chunkFilename: "static/js/[id].[chunkhash].js"
    },
    plugins: [
        // http://vuejs.github.io/vue-loader/en/workflow/production.html
        new Dotenv({
            path: "./.env.prod",
            safe: false
        }),
        new ExtractTextPlugin("css/[name].[contenthash].css"),
        // generate dist index.html with correct asset hash for caching.
        // you can customize output by editing /index.html
        // see https://github.com/ampedandwired/html-webpack-plugin
        new HtmlWebpackPlugin({
            filename: path.resolve(__dirname, "../dist/index.html"),
            template: "index.html",
            inject: true,
            minify: {
                removeComments: true,
                collapseWhitespace: true,
                removeAttributeQuotes: true
            },
            // necessary to consistently work with multiple chunks via CommonsChunkPlugin
            chunksSortMode: "dependency"
        })
    ]
})

module.exports = webpackConfig
