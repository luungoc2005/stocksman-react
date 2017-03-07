import React from 'react';

import DropDownMenu from 'material-ui/DropDownMenu';
import MenuItem from 'material-ui/MenuItem';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';

import $ from 'jquery';

import PriceList from './price-list'

const TOPSTOCKS_URL = "/stocks/top_stocks/{1}";
const GETINDICES_URL = "/stocks/ref/get_indices";

export default class TopStocks extends React.Component {
    constructor() {
        super();
        this.state = {
            index_code: '',
            data: [],
            filters: [],
        }
    }

    setFilter(indexCode) {
        if (!indexCode || indexCode === 'All') indexCode = '';
        $.getJSON(TOPSTOCKS_URL.replace("{1}", indexCode), (response) => {
            let newState = this.state;
            newState.index_code = indexCode;
            newState.data = response;
            this.setState(newState);
        });
    }

    componentWillMount() {
        $.getJSON(GETINDICES_URL, (response) => {
            let newState = this.state;
            newState.filters = response;
            this.setState(newState);
        });
        this.setFilter();
    }

    render() {
        let filterList = this.state.filters.slice(0);
        let filterMenu = [];
        filterList.push('');
        for (let i = 0; i < filterList.length; i++) {
            filterMenu.push(
                <MenuItem
                    key={i}
                    value={filterList[i]}
                    primaryText={(!filterList[i]) ? 'ALL' : filterList[i]}
                />
            )
        }

        return (
            <Card>
                <CardHeader title="Top Performers:" />
                <CardText>
                    <PriceList 
                        data={this.state.data} 
                        showCode={true} 
                        showDate={false}
                        onItemSelected={(item) => this.props.onItemSelected?
                                        this.props.onItemSelected(item):undefined}
                    />
                </CardText>
                <CardActions>
                    <DropDownMenu value={this.state.index_code} onChange={(event, index, value) => this.setFilter(value)}>
                        {filterMenu}
                    </DropDownMenu>
                </CardActions>
            </Card>
        )
    }
}