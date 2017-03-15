import React from 'react';
import $ from 'jquery';

import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import {Table, TableBody, TableFooter, TableHeader, TableHeaderColumn, TableRow, TableRowColumn}
  from 'material-ui/Table';
import FlatButton from 'material-ui/FlatButton';

const STATUS_URL = "/stocks/status/";
const UPDATE_URL = "/stocks/update_all/";

export default class StatusTable extends React.Component {
    constructor() {
        super();
        this.state = {
            data: {},
            update: false,
        };
    }

    getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    componentDidMount() {
        this.refreshData();
    }

    refreshData() {
        $.getJSON(STATUS_URL, (response) => {
            this.setState({
                data: response,
                update: false,
            });
        });
    }

    postUpdate() {
        this.setState({update: true});
        $.post(UPDATE_URL, () => {
            this.refreshData()
        });
    }

    render() {
        let data = this.state.data;

        function formatDate(date) {
            return date?new Date(date).toString():''
        }

        function formatAccuracy(number) {
            return (number)? `${(Math.round(number * 10000) / 100)}%` : ''
        }

        function getDate(date) {
            let d = new Date(date);
            d.setHours(0,0,0,0);
            return d;
        }

        let today = getDate(Date.now());

        let updateButtonDisabled = (
            this.state.update ||
            !data.data_date ||
            !data.clf_date ||
            !data.rg_date ||
            getDate(data.data_date) >= today
        );

        return(
            <Card>
                <CardHeader
                    title = "Database Status"
                />
                <CardText>
                    <Table>
                        <TableHeader
                            adjustForCheckbox={false}
                            displaySelectAll={false}
                        >
                            <TableHeaderColumn>Item</TableHeaderColumn>
                            <TableHeaderColumn>Date</TableHeaderColumn>
                            <TableHeaderColumn>Accuracy</TableHeaderColumn>
                        </TableHeader>
                        <TableBody
                            displayRowCheckbox={false}
                        >
                            <TableRow>
                                <TableRowColumn>PRICE DATA</TableRowColumn>
                                <TableRowColumn>
                                    {formatDate(data.data_date)}
                                </TableRowColumn>
                                <TableRowColumn>
                                </TableRowColumn>
                            </TableRow>
                            <TableRow>
                                <TableRowColumn>CLF MODEL</TableRowColumn>
                                <TableRowColumn>
                                    {formatDate(data.clf_date)}
                                </TableRowColumn>
                                <TableRowColumn>
                                    {formatAccuracy(data.clf_accuracy)}
                                </TableRowColumn>
                            </TableRow>
                            <TableRow>
                                <TableRowColumn>RG MODEL</TableRowColumn>
                                <TableRowColumn>
                                    {formatDate(data.rg_date)}
                                </TableRowColumn>
                                <TableRowColumn>
                                    {formatAccuracy(data.rg_accuracy)}
                                </TableRowColumn>
                            </TableRow>
                        </TableBody>
                    </Table>
                </CardText>
                <CardActions>
                    <FlatButton 
                        label='UPDATE ALL'
                        disabled={updateButtonDisabled}
                        onTouchTap={() => this.postUpdate()}
                    />
                </CardActions>
            </Card>
        );
    }
}