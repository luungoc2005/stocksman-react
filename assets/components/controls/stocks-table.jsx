import React from 'react';
import {Table, TableBody, TableFooter, TableHeader, TableHeaderColumn, TableRow, TableRowColumn}
  from 'material-ui/Table';

export default function StocksTable(props) {
    let data = props.data || []
    let headdata = props.header || []
    
    let header = [];
    let rows = [];
    if (data.length > 0 && data[0].length > 1) {
        for (let i = 0; i < data.length; i++) {
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
    
    if (props.header && props.header.length > 0) {
        for (let i = 0; i < headdata.length; i++) {
            header.push(
                <TableHeaderColumn key={i}>
                    {headdata[i]}
                </TableHeaderColumn>
            );
        }
    }

    return (
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
    );
}