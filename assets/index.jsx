'use strict';

import $ from 'jquery';  
import ReactDOM from 'react-dom';
import React from 'react';

// themes
import normalize from './css/normalize.css';
import toast from './css/toast.css'; // Grids
import styles from './css/style.css';

import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import {deepPurple100, deepPurple500, deepPurple700} from 'material-ui/styles/colors';

// React components
import Navbar from './components/navbar';
import Footer from './components/footer';
import App from './components/app';
import Initializer from './components/initializer'

import {
  BrowserRouter as Router,
  Route,
} from 'react-router-dom'

import injectTapEventPlugin from 'react-tap-event-plugin';
// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

const muiTheme = getMuiTheme({
  palette: {
    primary1Color: deepPurple500,
    primary2Color: deepPurple700,
    primary3Color: deepPurple100,
  },
}, {
  avatar: {
    borderColor: null,
  },
});

ReactDOM.render(
  <div className={styles.wrap}>
    <Initializer />
    <MuiThemeProvider muiTheme={muiTheme}>
      <Navbar />
    </MuiThemeProvider>
    <MuiThemeProvider muiTheme={muiTheme}>
      <Router>
        <div>
          <Route path={`/:tabIndex`} component={App}/>
          <Route exact path="/" component={App}/>
        </div>
      </Router>
    </MuiThemeProvider>
    <MuiThemeProvider muiTheme={muiTheme}>
      <Footer />
    </MuiThemeProvider>
  </div>,
  document.getElementById('content')
);