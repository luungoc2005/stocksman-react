import React from 'react';

import toast from '../css/toast.css'; // Grids
import styles from '../css/style.css';

class Footer extends React.Component {
    render() {
/*            <Paper zDepth={1} className={[styles.footer, toast.grid].join(' ')}>
                <p>Footer content</p>
                <p>Paragraph 1 of footer content</p>
            </Paper>*/
        return (
            <div className={[styles.footer, toast.grid].join(' ')}>
                <div className={[toast.gridCol, toast.gridCol6Of12].join(' ')}>
                    <p>Made by <a href="https://luungoc2005.github.io/">luungoc2005</a></p>
                    <p>Check out the Github repo <a href="https://github.com/luungoc2005/stocksman-react">here</a></p>
                </div>
                <div className={[toast.gridCol, toast.gridCol6Of12].join(' ')}>
                    <p>Dependencies:Django and ReactJs with Material UI</p>
                </div>
            </div>
        );
    }
}

export default Footer;