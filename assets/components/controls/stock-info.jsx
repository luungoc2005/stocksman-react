import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import {List, ListItem} from 'material-ui/List';
import FlatButton from 'material-ui/FlatButton';
import ActionTrendingUp from 'material-ui/svg-icons/action/trending-up';
import ActionTrendingDown from 'material-ui/svg-icons/action/trending-down';
import ActionTrendingFlat from 'material-ui/svg-icons/action/trending-flat';
import {lightGreen500, deepOrange500, amber500} from 'material-ui/styles/colors';

import $ from 'jquery';

const STOCK_URL = "/stocks/get_stock/{1}";

export default class StockInfo extends React.Component {
    constructor() {
        super();
        this.state = {
            close_price: 0,
            close_date: "",
            oscillate: 0,
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

    formatCurrency(text) {
        return "VND " + text.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
    }

    render () {
        let stock_data = this.state;
        let history_list = [];
        
        let trendingIcon = (oscillate) => {
            if (oscillate > 0) {
                return (<ActionTrendingUp color={lightGreen500} />);
            } else if (oscillate < 0) {
                return (<ActionTrendingDown color={deepOrange500} />);
            } else {
                return (<ActionTrendingFlat color={amber500} />);
            }
        }

        if (stock_data.prices.length > 0) {
            for (let i = 0; i < stock_data.prices.length; i++) {
                let price = stock_data.prices[i];
                price.close_date = parseInt(price.close_date);
                stock_data.prices[i] = price;
            }
            stock_data.prices.sort((a,b) => a.close_date-b.close_date);
            stock_data.prices.reverse();

            for (let i = 0; i < stock_data.prices.length; i++) {
                let price = stock_data.prices[i];
                history_list.push(
                    <ListItem
                        primaryText={this.formatCurrency(price.close_price)}
                        secondaryText={new Date(price.close_date).toString()}
                        leftIcon={trendingIcon(price.oscillate)}
                        key={i}
                    />
                );
            }
        }

        let default_price = {
            close_date:null,
            close_price:0,
            oscillate:0
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
                        Latest Price:{this.formatCurrency(latest_price.close_price)}
                        <List>{history_list}</List>
                    </div>
                </CardText>
                <CardActions>
                    <FlatButton label="Refresh" onTouchTap={() => this.refreshData()} />
                </CardActions>
            </Card>
        )
    }
}