import React from 'react';

import toast from '../css/toast.css'; // Grids
import styles from '../css/style.css';

import Paper from 'material-ui/Paper';
import SearchBox from './controls/search-box'

class App extends React.Component {
  render() {
    return (
      <div className={[styles.mainContent, toast.grid].join(' ')}>
        <SearchBox />
        <h1>Hello, World!</h1>
      </div>
    );
  }
}

export default App;