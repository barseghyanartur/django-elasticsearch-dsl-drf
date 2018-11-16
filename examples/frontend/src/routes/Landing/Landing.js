import React, { Fragment } from 'react';
import PropTypes from 'prop-types';
import './Landing.css';
import history from '../../history';


class Landing extends React.Component {

    static propTypes = {
        history: PropTypes.object,
    };

    constructor(props) {
        super(props);
        this.state = {
            query: '',
        };
        this.onSubmit = this.onSubmit.bind(this);
        this.onChange = this.onChange.bind(this);
    }

    onSubmit(event) {
        event.preventDefault();
        this.props.updateQuery(this.state.query);
        history.push(`/search/?query=${this.state.query}`);
    }

    onChange(event) {
        event.preventDefault();
        this.setState({
            [event.currentTarget.name]: event.currentTarget.value
        });
    }

    render() {
        const { updateQuery } = this.props;
        console.log(this.props);
        return (
            <Fragment>
                <div className="landing-wrapper">
                    <form onSubmit={this.onSubmit}>
                        <label>Query</label>
                        <input key="query"
                               name="query"
                               defaultValue={this.state.query}
                               onChange={this.onChange} />

                        <button type="submit">Search</button>
                    </form>
                </div>
            </Fragment>
        )
    }
}


export default Landing;
