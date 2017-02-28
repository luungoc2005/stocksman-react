'use strict';

var $ = require('jquery');  
var ReactDOM = require('react-dom');
var React = require('react');
var App = require('./app');

ReactDOM.render(
  React.createElement(App, null),
  document.getElementById('content')
);