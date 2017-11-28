const webpack = require("webpack")
const merge = require("webpack-merge")
const baseWebpackConfig = require("./webpack.base.conf")
const HtmlWebpackPlugin = require("html-webpack-plugin")
const Dotenv = require("dotenv-webpack");

module.exports = merge(baseWebpackConfig, {
    module: {
        rules: [{
            test: /\.css$/,
            use: [{
                loader: "style-loader"
            }, {
                loader: "css-loader"
            }]
        }, {
            test: /\.vue$/,
            loader: 'vue-loader',
            options: {
                esModule: true,
                postcss: [
                    require('autoprefixer')({
                        browsers: ['last 2 versions']
                    })
                ]
            }
        }]
    },
    devtool: "source-map",
    plugins: [
        new Dotenv({
            path: './.env.dev',
            safe: false
        }),

        // https://github.com/glenjamin/webpack-hot-middleware#installation--usage
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(),
        // https://github.com/ampedandwired/html-webpack-plugin
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: 'index.html',
            inject: true
        })
    ]
})
