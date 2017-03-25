import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import Chip from 'material-ui/Chip';
import {lightGreen100, deepOrange100, amber100, blue900} from 'material-ui/styles/colors';
import {ResponsiveContainer, LineChart, Line, CartesianGrid, Tooltip, XAxis} from 'recharts'

import PriceList from './price-list'

import $ from 'jquery';

const STOCK_URL = "/stocks/get_stock/{1}/";
const PREDICT_URL = "/stocks/project_stock/{1}/"

export default class StockInfo extends React.Component {
    constructor() {
        super();
        this.state = {
            data: [],
            predict: [],
            chart_data: [],
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
                let chart_data = [];

                if (data.prices !== undefined && data.prices.length > 0) {
                    for (let i = 0; i < data.prices.length; i++) {
                        let price = data.prices[i];
                        price.close_date = parseInt(price.close_date);
                        
                        // for chart tooltip
                        let date = new Date(price.close_date);
                        //price.name="d/m".replace("d", date.getDate()).replace("m", date.getMonth());
                        price.name=date.toLocaleDateString();

                        data.prices[i] = price;
                    }
                    data.prices.sort((a,b) => b.close_date-a.close_date);
                    chart_data = data.prices.slice();
                    chart_data.reverse();
                }

                data.chart_data = chart_data;

                this.setState({
                    data: data,
                });
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

        let predictedString = ''
        if (this.state.predict) {
            predictedString = `Predicted: ${formatCurrency(this.state.predict.adj_price)} (${Math.round(this.state.predict.prob_positive * 10000) / 100}% to increase)`
        }

        return (
            <Card>
                <CardHeader
                    title={stock_data.stock_code}
                    subtitle={`${stock_data.company_name} - ${stock_data.index}`}
                />
                <CardMedia>
                    <ResponsiveContainer width="100%" aspect={4.0/1.0}>
                        <LineChart data={stock_data.chart_data}>
                            <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="name" hide={true} />
                                <Line name="Close Price" type='monotone' dataKey='close_price' stroke={blue900} strokeWidth={2} />
                            <Tooltip />
                        </LineChart>
                    </ResponsiveContainer>
                </CardMedia>
                <CardText>
                    <div>
                        <span>Latest Price: {formatCurrency(latest_price.close_price)}
                            <Chip backgroundColor={predict_color}>
                                {predictedString}                        
                            </Chip>
                        </span>
                        <PriceList data={stock_data.prices} showDate={true} limit={5} />
                    </div>
                </CardText>
                <CardActions>
                    <FlatButton label="Refresh" onTouchTap={() => this.refreshData()} />
                </CardActions>
            </Card>
        )
    }
}