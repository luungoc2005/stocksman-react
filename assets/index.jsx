'use strict';

import $ from 'jquery';  
import ReactDOM from 'react-dom';
import React from 'react';

// themes
import normalize from './css/normalize.css';
import toast from './css/toast.css'; // Grids
import styles from './css/style.css';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import injectTapEventPlugin from 'react-tap-event-plugin';

// React components
import Navbar from './components/navbar';
import Footer from './components/footer';
import App from './components/app';

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

ReactDOM.render(
  <div className={styles.wrap}>
    <MuiThemeProvider>
      <Navbar />
    </MuiThemeProvider>
    <MuiThemeProvider>
      <App />
    </MuiThemeProvider>
    <MuiThemeProvider>
      <Footer />
    </MuiThemeProvider>
  </div>,
  document.getElementById('content')
);