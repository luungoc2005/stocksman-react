import React from 'react';

import toast from '../css/toast.css'; // Grids
import styles from '../css/style.css';

import Paper from 'material-ui/Paper';
import {Tabs, Tab} from 'material-ui/Tabs';

import SearchBox from './controls/search-box'
import StockInfo from './controls/stock-info'
import TopStocks from './controls/top-stocks'
import EventsList from './controls/events-list'
import PredictTable from './predict-table'
import StatusTable from './status-table'

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      selected_stock: "",
    }
  }

  onSearchInput(item) {
    this.setState({
      selected_stock: item,
    })
  }

  render() {
    let text = this.state.selected_stock;
    return (
      <Tabs
        className={[toast.grid, styles.marginTop10].join(' ')}
        value={this.props.tabIndex}
      >
        <Tab label="Market Status" value={0}>          
          <div className={[styles.mainContent, toast.grid, styles.marginTop20].join(' ')}>
            <div className={[toast.gridCol, toast.gridCol6Of12].join(' ')}>
              <SearchBox onUpdateInput={(item) => this.onSearchInput(item.text)} />
              <StockInfo stockCode={text} />
            </div>
            <div className={[toast.gridCol, toast.gridCol6Of12].join(' ')}>
              <div>
                <TopStocks
                  onItemSelected={(item) => this.onSearchInput(item)}
                />
              </div>
              <div className={styles.marginTop10}>
                <EventsList                  
                  onItemSelected={(item) => this.onSearchInput(item)}
                />
              </div>
            </div>
          </div>
        </Tab>
        <Tab label="Predictions" value={1}>          
          <div className={[styles.mainContent, toast.grid, styles.marginTop10].join(' ')}>
            <div className={[toast.gridCol, toast.gridCol12Of12].join(' ')}>
              <PredictTable />
            </div>
          </div>
        </Tab>
        <Tab label="Maintenance" value={2}>
          <div className={[styles.mainContent, toast.grid, styles.marginTop10].join(' ')}>
            <div className={[toast.gridCol, toast.gridCol12Of12].join(' ')}>
              <StatusTable />
            </div>
          </div>
        </Tab>
      </Tabs>
    );
  }
}

export default App;