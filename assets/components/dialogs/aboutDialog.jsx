import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import IconButton from 'material-ui/IconButton';
import ActionHelp from 'material-ui/svg-icons/action/help';
import {grey50} from 'material-ui/styles/colors';

export default class AboutDialog extends React.Component {
    constructor() {
        super();
        this.state = {open: false};
    }

    render() {
        return (
            <IconButton onTouchTap={() => this.setState({open: true})}>
                <ActionHelp color={grey50} />
                <Dialog
                    title="About"
                    actions={
                    <FlatButton
                        label="Close"
                        primary={true}
                        keyboardFocused={true}
                        onTouchTap={() => this.setState({open: false})}
                    />
                    }
                    modal={false}
                    open={this.state.open}
                    onRequestClose={() => this.setState({open: false})}
                >
                    Made by luungoc2005
                </Dialog>
            </IconButton>
        );
    }
}