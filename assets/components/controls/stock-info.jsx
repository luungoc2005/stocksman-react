import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import PriceList from './price-list'

import $ from 'jquery';

const STOCK_URL = "/stocks/get_stock/{1}";

export default class StockInfo extends React.Component {
    constructor() {
        super();
        this.state = {
            close_price: 0,
            close_date: "",
            oscillate: 0,
            oscillate_percent: 0,
            prices: []
        };
    }

    componentWillReceiveProps(nextProps) {
        if (this.props.stockCode != nextProps.stockCode) {
            this.getStockData(nextProps.stockCode);
        }
    }

    refreshData() {
        this.getStockData(this.props.stockCode);
    }

    getStockData(query) {
        if (query.length === 3) {
            $.getJSON(STOCK_URL.replace("{1}", query)).done((data) => {
                this.setState(data);
            });
        }
    }

    render () {
        let stock_data = this.state;
        
        let formatCurrency = (text) => {
            return "VND " + text.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
        }
        
        if (stock_data.prices.length > 0) {
            for (let i = 0; i < stock_data.prices.length; i++) {
                let price = stock_data.prices[i];
                price.close_date = parseInt(price.close_date);
                stock_data.prices[i] = price;
            }
            stock_data.prices.sort((a,b) => a.close_date-b.close_date);
            stock_data.prices.reverse();
        }

        let default_price = {
            close_date:null,
            close_price:0,
            oscillate:0,
            oscillate_percent: 0,
        }

        let latest_price = (stock_data.prices.length > 0)?stock_data.prices[0]:default_price;

        return (
            <Card>
                <CardHeader
                    title={stock_data.stock_code}
                    subtitle={stock_data.index}
                />
                <CardText>
                    <div>
                        Latest Price: {formatCurrency(latest_price.close_price)}
                        <PriceList data={stock_data.prices} showDate={true} />
                    </div>
                </CardText>
                <CardActions>
                    <FlatButton label="Refresh" onTouchTap={() => this.refreshData()} />
                </CardActions>
            </Card>
        )
    }
}