import React from 'react';

import DropDownMenu from 'material-ui/DropDownMenu';
import MenuItem from 'material-ui/MenuItem';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Toggle from 'material-ui/Toggle';

import $ from 'jquery';

import PriceList from './price-list'

const TOPSTOCKS_URL = "/stocks/top_stocks/{1}";
const TOPSTOCKS_T3_URL = "/stocks/top_stocks_t3/{1}";
const GETINDICES_URL = "/stocks/ref/get_indices";

export default class TopStocks extends React.Component {
    constructor() {
        super();
        this.state = {
            index_code: '',
            t3: false,
            data: [],
            filters: [],
        }
    }

    setFilter(indexCode, t3) {
        if (indexCode === null || indexCode === undefined) indexCode = this.state.index_code;
        
        let url = ''
        t3 = (t3 === null || t3 === undefined)? this.state.t3: t3

        if (t3 === true) {
            url = TOPSTOCKS_T3_URL.replace("{1}", indexCode);
        }
        else
        {
            url = TOPSTOCKS_URL.replace("{1}", indexCode);
        }

        $.getJSON(url, (response) => {
            this.setState({
                index_code: indexCode,
                data: response
            });
        });
    }

    componentWillMount() {
        $.getJSON(GETINDICES_URL, (response) => {
            this.setState({
                filters: response
            });
        });
        this.setFilter();
    }

    handleT3Toggle(event, isInputChecked) {
        this.setState({
            t3: isInputChecked
        });
        this.setFilter('', isInputChecked)
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
                <CardHeader title="Top Performers" />
                <CardText>                    
                    <Toggle
                        label="Enable T+3"
                        onToggle={(e,c) => this.handleT3Toggle(e,c)}
                    />
                </CardText>
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