import React from 'react';
import {Table, TableBody, TableFooter, TableHeader, TableHeaderColumn, TableRow, TableRowColumn}
  from 'material-ui/Table';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';

export default function StocksTable(props) {
    let data = props.data || []
    
    let header = [];
    let rows = [];
    if (data.length > 1 && data[0].length > 1) {
        for (let i = 0; i < data[0].length; i++) {
            header.push(
                <TableHeaderColumn>
                    {data[0][i]}
                </TableHeaderColumn>
            );
        }
        for (let i = 1; i < data.length; i++) {
            let tableRow = data[i];
            if (tableRow.length > 0) {
                let rowColumns = [];
                for (let a = 0; a < tableRow.length; a++) {
                    rowColumns.push(
                        <TableRowColumn key={a}>
                            {tableRow[a]}
                        </TableRowColumn>
                    );
                }
                rows.push(
                    <TableRow key={i}>
                        {rowColumns}
                    </TableRow>
                );
            }
        }
    }

    return (
        <Card>
            <CardHeader
                title = {props.tableTitle}
            />
            <CardText>
                <Table
                    height = {props.height}>
                    <TableHeader
                        adjustForCheckbox={false}
                        displaySelectAll={false}
                    >
                        <TableRow>
                            {header}
                        </TableRow>
                    </TableHeader>
                    <TableBody
                        displayRowCheckbox={false}
                    >
                        {rows}
                    </TableBody>
                </Table>
            </CardText>
        </Card>
    );
}