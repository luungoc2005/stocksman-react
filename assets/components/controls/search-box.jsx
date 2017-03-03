import React from 'react';
import AutoComplete from 'material-ui/AutoComplete';
import MenuItem from 'material-ui/MenuItem';

import $ from 'jquery';

const SEARCH_URL = "/stocks/find_stock/{1}/10";

export default class SearchBox extends React.Component {
    constructor() {
        super();
        this.state = {
            query: "",
            results: [],
        }
    }

    getSearchData(value) {
        if (0 < value.length && value.length < 3) {
            $.getJSON(SEARCH_URL.replace("{1}", value), (data) => {
                this.setState({
                    query: value,
                    results: data,
                });
            });
        }
        else {
            this.setState({
                query: value,
                results: [],
            });
        }
        return;
    }

    render() {
        let suggest_list = [];
        let data = this.state.results;
        if (data.length > 0) {
            for (let i = 0; i < data.length; i++) {
                suggest_list.push({
                    text: data[i].stock_code,
                    value: (
                    <MenuItem
                        primaryText={data[i].stock_code}
                        secondaryText={data[i].index}
                    />)
                });
            };
        };

        return (
            <AutoComplete 
                hintText="Search..."
                fullWidth={true}
                filter={AutoComplete.noFilter}
                dataSource={suggest_list}
                onUpdateInput={(text) => this.getSearchData(text)}
            />
        )
    }
}