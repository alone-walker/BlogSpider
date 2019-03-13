const webpack = require("webpack");
const path = require("path");
const TerserPlugin = require('terser-webpack-plugin');

const configuration = {};
const jspath = path.resolve(__dirname);

module.exports = {
  entry: {
    day: jspath + "/day.js",
    blog: jspath + "/blog.js",
    entries: jspath + "/entries.js",
    vote: jspath + "/vote.js",
    rss: jspath + "/rss.js",
    spiders: jspath + "/spiders.js"
  },

  output: {
    path: jspath + "/../script/",
    filename: "[name].js",
  },

  module: {
    rules: [{
      test: /\.js/,
      exclude: [/node_modules/, /spider_.*_pb.js/],
      loader: "babel-loader",
      options: {
        presets: [
          '@babel/preset-env',
          '@babel/preset-react',
          {
             plugins: ['@babel/plugin-proposal-class-properties'],
          }
        ]
      },
    }]
  },

  optimization: {
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          warnings: false,
          compress: {},
          parse: {},
          mangle: true,
        }
      })
    ]
  },
};
