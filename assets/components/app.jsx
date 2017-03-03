import React from 'react';

import toast from '../css/toast.css'; // Grids
import styles from '../css/style.css';

import Paper from 'material-ui/Paper';
import SearchBox from './controls/search-box'
import StockInfo from './controls/stock-info'

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      selected_stock: "",
    }
  }

  onSearchInput(item) {
    let current_state = this.state;
    current_state.selected_stock = item.text;
    this.setState(current_state)
  }

  render() {
    let text = this.state.selected_stock;
    return (
      <div className={[styles.mainContent, toast.grid].join(' ')}>
        <SearchBox onUpdateInput={(item) => this.onSearchInput(item)} />
        <StockInfo stockCode={text} />
      </div>
    );
  }
}

export default App;