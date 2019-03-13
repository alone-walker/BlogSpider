#! /usr/bin/env bash

npm init -f

npm install google-protobuf --save-dev
npm install grpc-web --save-dev
npm install react --save-dev
npm install react-dom --save-dev
npm install whatwg-fetch --save-dev
npm install @babel/core --save-dev
npm install @babel/preset-env --save-dev
npm install @babel/preset-react --save-dev
npm install @babel/plugin-proposal-class-properties --save-dev
npm install webpack --save-dev
npm install webpack-cli --save-dev
npm install babel-loader --save-dev
npm install terser-webpack-plugin --save-dev

node_modules/.bin/webpack --mode production --config webpack.config.js
