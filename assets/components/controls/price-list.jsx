import React from 'react';
import ActionTrendingUp from 'material-ui/svg-icons/action/trending-up';
import ActionTrendingDown from 'material-ui/svg-icons/action/trending-down';
import ActionTrendingFlat from 'material-ui/svg-icons/action/trending-flat';
import {lightGreen500, deepOrange500, amber500} from 'material-ui/styles/colors';
import {List, ListItem} from 'material-ui/List';

export default function PriceList(props) {
    let trendingIcon = (oscillate) => {
        if (oscillate > 0) {
            return (<ActionTrendingUp color={lightGreen500} />);
        } else if (oscillate < 0) {
            return (<ActionTrendingDown color={deepOrange500} />);
        } else {
            return (<ActionTrendingFlat color={amber500} />);
        }
    }

    let formatCurrency = (text) => {
        return "VND " + text.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
    }
    
    let history_list = [];
    let data_list = (props.data !== undefined) ? props.data.slice() : [];

    for (let i = 0; i < data_list.length; i++) {
        let price = data_list[i];
        history_list.push(
            <ListItem
                primaryText={`${props.showCode?price.stock_code+': ':''}${formatCurrency(price.close_price)} (${price.oscillate_percent}%)`}
                secondaryText={props.showDate?new Date(price.close_date).toString():''}
                leftIcon={trendingIcon(price.oscillate)}
                key={i}
                onClick={() => props.onItemSelected?
                props.onItemSelected(data_list[i].stock_code):undefined}
            />
        );
    }

    return (
        <List>{history_list}</List>
    );
}