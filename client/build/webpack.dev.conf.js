const webpack = require("webpack")
const merge = require("webpack-merge")
const baseWebpackConfig = require("./webpack.base.conf")
const HtmlWebpackPlugin = require("html-webpack-plugin")
const Dotenv = require("dotenv-webpack");

module.exports = merge(baseWebpackConfig, {
    devtool: "source-map",
    plugins: [
        new Dotenv({
            path: './.env.dev',
            safe: false
        }),
        // https://github.com/ampedandwired/html-webpack-plugin
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: 'index.html',
            inject: true
        })
    ]
})
