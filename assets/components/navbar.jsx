import React from 'react';

import toast from '../css/toast.css'; // Grids

import AppBar from 'material-ui/AppBar';
import AboutDialog from './dialogs/aboutDialog';

class Navbar extends React.Component {
  render() {
    return (
        <AppBar
            className={toast.grid}
            title="Stocks Machine Learning Experiment"
            iconElementRight=
            {
              <AboutDialog />
            }
        >
        </AppBar>
    );
  }
}

export default Navbar;