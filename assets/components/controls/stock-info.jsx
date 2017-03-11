import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import PriceList from './price-list'
import Chip from 'material-ui/Chip';
import {lightGreen100, deepOrange100, amber100} from 'material-ui/styles/colors';

import $ from 'jquery';

const STOCK_URL = "/stocks/get_stock/{1}/";
const PREDICT_URL = "/stocks/project_stock/{1}/"

export default class StockInfo extends React.Component {
    constructor() {
        super();
        this.state = {
            data: [],
            predict: [],
        };
    }

    componentWillReceiveProps(nextProps) {
        if (this.props.stockCode != nextProps.stockCode) {
            this.getStockData(nextProps.stockCode);
            this.getPredictData(nextProps.stockCode);
        }
    }

    refreshData() {
        this.setState({ data: {}, predict: {} });
        this.getStockData(this.props.stockCode);
        this.getPredictData(this.props.stockCode);
    }

    getStockData(query) {
        if (query.length >= 3) {
            $.getJSON(STOCK_URL.replace("{1}", query)).done((data) => {
                this.setState({data: data});
            });
        }
    }

    getPredictData(query) {
        if (query.length >= 3) {
            $.getJSON(PREDICT_URL.replace("{1}", query)).done((data) => {
                this.setState({predict: data});
            });
        }
    }

    render () {
        let stock_data = this.state.data;
        
        let formatCurrency = (text) => {
            if (text) {
                return "VND " + text.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
            }
            else {
                return "";
            };
        };
        
        if (stock_data.prices !== undefined && stock_data.prices.length > 0) {
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

        let latest_price = (stock_data.prices !== undefined && stock_data.prices.length > 0)?stock_data.prices[0]:default_price;
        let predict_color = lightGreen100;
        let predicted_price = this.state.predict.adj_price || 0;
        
        if (predicted_price > latest_price.close_price) {
            predict_color = lightGreen100
        } else if (predicted_price = latest_price.close_price) {
            predict_color = deepOrange100
        } else {
            predict_color = amber100
        }

        return (
            <Card>
                <CardHeader
                    title={stock_data.stock_code}
                    subtitle={stock_data.index}
                />
                <CardText>
                    <div>
                        <span>Latest Price: {formatCurrency(latest_price.close_price)}
                            <Chip backgroundColor={predict_color}>
                                {'Predicted: ' + formatCurrency(this.state.predict.adj_price)}                            
                            </Chip>
                        </span>
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