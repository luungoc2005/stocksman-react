import React from 'react';
import $ from 'jquery';

import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import DropDownMenu from 'material-ui/DropDownMenu';
import MenuItem from 'material-ui/MenuItem';

import StocksTable from './controls/stocks-table';

const PREDICT_URL = "/stocks/project_all/";

export default class PredictTable extends React.Component {
    constructor() {
        super();
        this.state = {
            data: {},
            sort: 4,
        }
    }

    refreshData() {
        $.getJSON(PREDICT_URL, (response) => {
            this.setState({
                data: response
            });
        });
    }

    onSortChanged(value) {
        this.setState({
            sort: value,
        });
    }

    componentDidMount() {
        this.refreshData();
    }

    render() {
        let data = [];
        let columns = ["Stock Code", "Proba. Positive", "Current Price", "Predicted", "Predicted (adjusted)"]

        let source = this.state.data;
        if (source && source.length > 0) {
            for (let i = 0; i < source.length; i++) {                
                let row = [];
                let rowData = source[i];
                row.push(rowData.stock_code);
                row.push(Math.round(rowData.prob_positive * 10000) / 100) + " %";
                row.push(rowData.current_price);
                row.push(rowData.future_price);
                row.push(rowData.adj_price);
                data.push(row);
            }
        }

        let dropdownItems = columns.map((value, index) => {
            return (
                <MenuItem
                    key={index}
                    value={index}
                    primaryText={value}
                />
            );
        });

        switch (this.state.sort) {
            case 0:
                data.sort((a,b) => {
                    return a[0].localeCompare(b[0]);
                });
                break;
            case 1:
                data.sort((a, b) => {
                    return b[1] - a[1];
                });
                break;
            case 2:
                data.sort((a, b) => {
                    return b[2] - a[2];
                });
                break;
            case 3: // Future price
                data.sort((a, b) => {
                    let a_current = a[2];
                    let b_current = b[2];
                    let a_future = a[3];
                    let b_future = b[3];
                    let a_increase = a_future / a_current;
                    let b_increase = b_future / b_current;

                    return b_increase - a_increase;                    
                });
                break;
            case 4: // Adjusted Price
                data.sort((a, b) => {
                    let a_current = a[2];
                    let b_current = b[2];
                    let a_future = a[4];
                    let b_future = b[4];
                    let a_increase = a_future / a_current;
                    let b_increase = b_future / b_current;

                    return b_increase - a_increase;
                });
                break;
            default:
                break;
        }

        return (            
            <Card>
                <CardHeader
                    title = "Predicted Stock Prices"
                />
                <CardText>
                    <StocksTable
                        height="300px"
                        header={columns}
                        data={data}
                    />
                </CardText>
                <CardActions>
                    <DropDownMenu
                        value={this.state.sort}
                        onChange={(event, query) => this.onSortChanged(query)}
                    >
                        {dropdownItems}
                    </DropDownMenu>
                </CardActions>
            </Card>
        )
    }
}