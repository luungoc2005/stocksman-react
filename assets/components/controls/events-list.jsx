import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import $ from 'jquery'

import PriceList from './price-list'

const EVENTS_URL = "stocks/events/";

export default class EventsList extends React.Component {
    constructor() {
        super();
        this.state = {
            data: [],
            expanded: true,
        }
    }

    handleExpandChange(expanded) {
        this.setState({expanded: expanded});
    }

    componentDidMount() {
        this.refreshData();
    }

    refreshData() {
        $.getJSON(EVENTS_URL, (data) => {
            this.setState({data: data});
        });
    }

    render() {
        return(
            <Card expanded={this.state.expanded} onExpandChange={(expanded) => this.handleExpandChange(expanded)}>
                <CardHeader title="Events" actAsExpander={true} showExpandableButton={true} />
                <CardText expandable={true}>
                    <PriceList 
                        data={this.state.data} 
                        showCode={true}
                        showDate={false}
                        onItemSelected={(item) => this.props.onItemSelected?
                                        this.props.onItemSelected(item):undefined}
                    />
                </CardText>
                <CardActions expandable={true}>
                    <FlatButton label="Refresh" onTouchTap={() => this.refreshData()} />
                </CardActions>
            </Card>
        );
    }
}