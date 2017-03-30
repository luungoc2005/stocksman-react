import React from 'react';

import toast from '../css/toast.css'; // Grids
import styles from '../css/style.css';

import Paper from 'material-ui/Paper';
import {Tabs, Tab} from 'material-ui/Tabs';
import {Link} from 'react-router-dom';

import SearchBox from './controls/search-box';
import StockInfo from './controls/stock-info';
import TopStocks from './controls/top-stocks';
import EventsList from './controls/events-list';
import PredictTable from './predict-table';
import StatusTable from './status-table';

// tabs route naming
const TAB_STATUS="status";
const TAB_PREDICTIONS="predictions";
const TAB_MAINTENANCE="maintenance";

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
    let tabIndex = (this.props.match.params)?this.props.match.params.tabIndex:TAB_STATUS;

    return (
      <Tabs
        className={[toast.grid, styles.marginTop10].join(' ')}
        value={tabIndex}
      >
        <Tab
          label="Market Status"
          value={TAB_STATUS}
          containerElement={
            <Link to={`/${TAB_STATUS}`} />
          }
        >
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
        <Tab
          label="Predictions"
          value={TAB_PREDICTIONS}
          containerElement={
            <Link to={`/${TAB_PREDICTIONS}`} />
          }
        >
          <div className={[styles.mainContent, toast.grid, styles.marginTop10].join(' ')}>
            <div className={[toast.gridCol, toast.gridCol12Of12].join(' ')}>
              <PredictTable />
            </div>
          </div>
        </Tab>
        <Tab
          label="Maintenance"
          value={TAB_MAINTENANCE}
          containerElement={
            <Link to={`/${TAB_MAINTENANCE}`} />
          }
        >
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