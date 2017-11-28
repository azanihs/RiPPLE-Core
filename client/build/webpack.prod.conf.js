const path = require("path")
const webpack = require("webpack")
const merge = require("webpack-merge")
const baseWebpackConfig = require("./webpack.base.conf")
const ExtractTextPlugin = require("extract-text-webpack-plugin")
const HtmlWebpackPlugin = require("html-webpack-plugin")
const Dotenv = require("dotenv-webpack");

const extractCSS = new ExtractTextPlugin("[name].[contenthash].css");
const cssAutoprefixer = require("autoprefixer");
var webpackConfig = merge(baseWebpackConfig, {
    module: {
        rules: [{
            test: /\.css$/,
            use: extractCSS.extract({
                use: ["css-loader"],
                fallback: "style-loader"
            })
        }, {
            test: /\.vue$/,
            loader: "vue-loader",
            options: {
                esModule: true,
                loaders: {
                    css: extractCSS.extract({
                        use: "css-loader",
                        fallback: "vue-style-loader"
                    })
                },
                postcss: [
                    cssAutoprefixer({
                        browsers: ["last 2 versions"]
                    })
                ]
            }
        }]
    },
    devtool: "#source-map",
    output: {
        path: path.resolve(__dirname, '../dist'),
        filename: "static/js/[name].[chunkhash].js",
        chunkFilename: "static/js/[id].[chunkhash].js"
    },
    plugins: [
        extractCSS,
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
