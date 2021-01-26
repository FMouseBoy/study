const path = require('path')
const htmlWebpackPlugin = require('html-webpack-plugin')
module.exports = {
  entry: path.join(__dirname, './src/main.js'),
  output: {
    path: path.join(__dirname, './dist'),
    filename: 'app.js'
  },
  mode: 'development',
  plugins: [
    new htmlWebpackPlugin({
      Template: path.join(__dirname, './src/index.html')
    }),
  ],
  devServer: {
    open: false,
    port: 3613,
    compress: true,
    hot: true
  },
  module: {
    rules: [
      { test: /\.css$/, use: ["style-loader", "css-loader"]},
      { test: /\.less$/, use: ["style-loader", "css-loader", "less-loader"]},
      { test: /\.js$/, use: "babel-loader", exclude: /node_modules/}
    ]
  }
}