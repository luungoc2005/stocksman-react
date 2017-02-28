var React = require('react');
var styles = require('./css/style.css');

var App = React.createClass({
  render: function() {
    return (
      <div className={styles.app}>
        <h1>Hello, World!</h1>
      </div>
    );
  }
});

module.exports = App;