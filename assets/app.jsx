import React from 'react';

import toast from './css/toast.css'; // Grids

import styles from './css/style.css';

class App extends React.Component {
  render() {
    return (
      <div className={toast.grid}>
        <h1>Hello, World!</h1>
      </div>
    );
  }
}

export default App;