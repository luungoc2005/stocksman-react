import React from 'react';
import $ from 'jquery';

import StocksTable from './controls/stocks-table';

const PREDICT_URL = "/stocks/project_all/";

export default class PredictTable extends React.Component {
    constructor() {
        super();
        this.state = {
            data: {}
        }
    }

    refreshData() {
        $.getJSON(PREDICT_URL, (response) => {
            this.setState({
                data: response
            });
        });
    }

    componentDidMount() {
        this.refreshData();
    }

    render() {
        let data = [];
        let columns = ["Stock Code", "Proba. Positive", "Current Price", "Predicted Price", "Predicted Price (adjusted)"]

        if (this.state.data && this.state.data.length > 0) {
            for (let i = 0; i < this.state.data.length; i++) {
                let row = [];
                let rowData = this.state.data[i];
                row.push(rowData.stock_code);
                row.push(Math.round(rowData.prob_positive * 100) / 100);
                row.push(rowData.current_price);
                row.push(rowData.future_price);
                row.push(rowData.adj_price);
                data.push(row);
            }
        }

        data.sort((a, b) => {
            let a_current = a[2];
            let b_current = b[2];
            let a_future = a[4];
            let b_future = b[4];
            let a_increase = a_future / a_current;
            let b_increase = b_future / b_current;

            if (a_increase > b_increase) {
                return -1;
            } else if (a_increase < b_increase) {
                return 1;
            } else {
                return 0;
            }
        });

        data.unshift(columns);

        return (
            <StocksTable
                tableTitle="Predicted Stock Prices"
                height="200px"
                data={data}
            />
        )
    }
}