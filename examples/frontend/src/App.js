import React, { Component } from 'react';
import {
    BrowserRouter,
    Route,
    Switch,
} from 'react-router-dom';

import Search from './routes/Search/Search';

import logo from './logo.svg';
import './App.css';

class App extends Component {

    constructor(props) {
        super(props);
        this.updateQuery = this.updateQuery.bind(this);
        this.state = {
            query: ''
        }
    }

    updateQuery(query) {
        this.setState({query});
    }

    render() {
    return (
        <BrowserRouter>
            <Switch>
                <Route
                    exact path="/"
                    component={
                        () => <Search
                                updateQuery={this.updateQuery}
                                { ...this.props }
                                { ...this.state }
                              />
                    }
                />
            </Switch>
        </BrowserRouter>
    );
    }
}

export default App;
