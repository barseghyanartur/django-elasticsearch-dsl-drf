import React, { Fragment } from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import Autosuggest from 'react-autosuggest'
import { debounce } from 'throttle-debounce'
import { DefaultButton, initializeIcons } from "office-ui-fabric-react";

import './Search.css';
import api from '../../api';
import constants from '../../constants';
import { getQueryStringParams } from '../../helpers';
import Result from '../../components/Result/Result';
import Filter from '../../components/Filter/Filter';
import Pagination from '../../components/Pagination/Pagination';

initializeIcons();

class Search extends React.Component {

    static propTypes = {
        history: PropTypes.object,
    };

    constructor(props) {
        super(props);
        this.state = {
            query: '',
            facets: {},
            filters: {},
            next: null,
            previous: null,
            results: [],
            page: 1,
            count: 0,
            suggestions: [],
        };
        this.onSubmit = this.onSubmit.bind(this);
        this.onButtonClick = this.onButtonClick.bind(this);
        this.doSearch = this.doSearch.bind(this);
//        this.onChange = this.onChange.bind(this);
        this.renderResults = this.renderResults.bind(this);
        this.renderFilters = this.renderFilters.bind(this);
        this.resetFilters = this.resetFilters.bind(this);
        this.updateFilters = this.updateFilters.bind(this);
        this.renderPagination = this.renderPagination.bind(this);
        this.updatePageNumber = this.updatePageNumber.bind(this);
        this.resetPageNumber = this.resetPageNumber.bind(this);
    }

    componentWillMount() {
        const queryParams = getQueryStringParams(window.location.search);
        if (queryParams.query) {
            this.setState({query: queryParams.query});
        }

        // Suggest
        this.onSuggestionsFetchRequested = debounce(
            500,
            this.onSuggestionsFetchRequested
        );
        // END suggest
    }

    /**
     * Render suggestions.
     */
    renderSuggestion = suggestion => {
        return (
            <div className="result">
                <div>{suggestion}</div>
            </div>
        )
    };

    /**
     * Suggestions.
     */
    suggestOnChange = (event, { newValue }) => {
        this.setState({ query: newValue });
    };

    /**
     * Suggestions.
     */
    onSuggestionsFetchRequested = ({ value }) => {
        api.suggest(value)
           .then(res => {
               console.log('res: ', res);
               let results = [];
               res.data[constants.api.suggester].map(s => {
                    s.options.map(h => {
                        results.push(h.text);
                    });
               });
               this.setState({ suggestions: results });
           });
    };

    /**
     * Suggestions.
     */
    onSuggestionsClearRequested = () => {
        this.setState({ suggestions: [] });
    };

    /**
     * Get suggestion value.
     */
    getSuggestionValue = (suggestion) => {
        return suggestion;
    };

    componentDidMount() {
        const { query, results } = this.state;
        if (query && this.state.results.length === 0) {
            this.doSearch();
        }
    }

    /**
     * Sends a request to the search backend (REST framework), then
     * updates the state.
     */
    doSearch(page=null) {
        const filters = this.updateFilters();
        const currentPage = page || this.state.page;
        api.search(this.state.query, filters, currentPage)
           .then((result) => {
               this.setState({
                   facets: result.data.facets,
                   next: result.data.next,
                   previous: result.data.previous,
                   results: result.data.results,
                   count: result.data.count,
               });
           });
    }

    /**
     * Rest filters.
     */
    resetFilters() {
        this.setState({
            filters: {},
            page: 1,
        });
        this.refs.filtersForm.reset();

    }

    /**
     * Search button click handler. Resets filter and performs the search.
     */
    onButtonClick(event) {
        event.preventDefault();
        this.props.history.push(`/?query=${this.state.query}`);
        this.resetFilters();
        this.doSearch();
    }

    /**
     * Update all filters.
     */
    updateFilters() {
        let filters = {};
        const formFilters = [].filter.call(
            document.getElementsByTagName('input'), (c) => c.checked
        ).map(c => [c.name, c.value]);
        formFilters.map((f) => {
            let filterName = f[0];
            let filterValue = f[1];
            if (filterName in filters) {
                if (filterValue in filters[filterName]) {
                } else {
                    filters[filterName][filterValue] = true;
                }
            } else {
                filters[filterName] = {[filterValue]: true};
            }
        });
        this.setState({
            filters: filters,
        });
        return filters;
    }

    /**
     * On form submit handler.
     */
    onSubmit(event) {
        event.preventDefault();
        this.props.updateQuery(this.state.query);
        this.doSearch();
    }

//    /**
//     * Search query field handler.
//     */
//    onChange(event) {
//        event.preventDefault();
//        this.setState({
//            [event.currentTarget.name]: event.currentTarget.value
//        });
//    }

    /**
     * Render results.
     */
    renderResults() {
        const { results, count, query } = this.state;
        const self = this;
        return (
            <Fragment>
                {count} hits that match your search criteria: {query}
                {
                    results.map(
                        function(result, index) {
                            return <Result key={index} {...result} globalState={self.state} />;
                        }
                    )
                }
            </Fragment>
        )
    }

    /**
     * Render filters.
     */
    renderFilters() {
        const { facets } = this.state;
        const doSearch = this.doSearch;
        const resetPageNumber = this.resetPageNumber;
        return (
            <Fragment>
                Results follow...
                <form ref="filtersForm">
                {
                    Object.values(facets).map(
                        function(filter, index) {
                            console.log('this: ', this);
                            return (
                                <Fragment>
                                    <Filter
                                        key={index}
                                        {...filter}
                                        doSearch={doSearch}
                                        resetPageNumber={resetPageNumber}
                                    />
                                </Fragment>
                            );
                        }
                    )
                }
                </form>
            </Fragment>
        )
    }

    /**
     * Update page number in the state and does the search.
     */
    updatePageNumber(page) {
        this.setState({page});
        this.doSearch(page);
    }

    /**
     * Set page number to 1.
     */
    resetPageNumber() {
        this.setState({page: 1});
    }

    /**
     * Render pagination.
     */
    renderPagination() {
        if (this.state.count > constants.api.searchPageSize) {
            return (
                <Fragment>
                    <Pagination count={this.state.count}
                                pageSize={constants.api.searchPageSize}
                                updatePageNumber={this.updatePageNumber}
                                currentPage={this.state.page}
                    />
                </Fragment>
            )
       }
    }

    /**
     * Render the Search component.
     */
    render() {
        // Suggestions
        const { query, suggestions } = this.state;

        const inputProps = {
            placeholder: 'customer name or short code',
            value: query,
            onChange: this.suggestOnChange,
        };
        // END suggestions

        const { updateQuery } = this.props;
        return (
            <Fragment>
                <div className="search-wrapper">
                    <div className="top-wrapper">
                        <h2>Search form</h2>
                        <form onSubmit={this.onSubmit}>
                            {/*
                            <label>Query</label>
                            <input key="query"
                                   name="query"
                                   defaultValue={this.state.query}
                                   onChange={this.onChange} />
                            */}
                            <div className="query-wrapper">
                                <Autosuggest
                                    suggestions={suggestions}
                                    onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
                                    onSuggestionsClearRequested={this.onSuggestionsClearRequested}
                                    getSuggestionValue={this.getSuggestionValue}
                                    renderSuggestion={this.renderSuggestion}
                                    inputProps={inputProps}
                                />
                            </div>

                            <button
                                className="search-button"
                                type="submit"
                                onClick={this.onButtonClick}>
                                Search
                            </button>
                        </form>
                    </div>
                    <div className="main-wrapper">
                        <div className="filters-wrapper">
                            <h2>Filters</h2>
                            {this.renderFilters()}
                        </div>
                        <div className="results-wrapper">
                            <div className="inner">
                            <h2>Results</h2>
                            {this.renderResults()}
                            {this.renderPagination()}
                            </div>
                        </div>
                    </div>
                </div>
            </Fragment>
        )
    }
}


export default withRouter(Search);
