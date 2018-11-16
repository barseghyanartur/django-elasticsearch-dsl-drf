import React, { Fragment } from 'react';
import { withRouter } from 'react-router-dom';
import './Search.css';
import api from '../../api';
import { getQueryStringParams } from '../../helpers';
import Result from '../../components/Result/Result';
import Filter from '../../components/Filter/Filter';


class Search extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            query: '',
            facets: {},
            filters: {},
            next: null,
            previous: null,
            results: [],
            page: 0,
            count: 0,
        };
        this.onSubmit = this.onSubmit.bind(this);
        this.onButtonClick = this.onButtonClick.bind(this);
        this.doSearch = this.doSearch.bind(this);
        this.onChange = this.onChange.bind(this);
        this.renderResults = this.renderResults.bind(this);
        this.renderFilters = this.renderFilters.bind(this);
        this.updateFilter = this.updateFilter.bind(this);
        this.resetFilters = this.resetFilters.bind(this);
        this.updateFilters = this.updateFilters.bind(this);
    }

    componentWillMount() {
        const queryParams = getQueryStringParams(window.location.search);
        if (queryParams.query) {
            this.setState({query: queryParams.query});
        }
    }

    doSearch() {
        console.log('this.state.filters!!!!!!!!!!', this.state.filters);
        const filters = this.updateFilters();
        api.searchBooks(this.state.query, filters)
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

    resetFilters() {
        this.setState({filters: {}});
        this.refs.filtersForm.reset();

    }

    onButtonClick(event) {
        event.preventDefault();
        this.resetFilters();
        this.doSearch();
    }

    /**
     * Update specific filter.
     */
    updateFilter(filterName, filterValue, remove=false) {
//        console.log('updateFilter');
//        console.log('filterName: ', filterName);
//        console.log('filterValue: ', filterValue);
//        console.log('remove: ', remove);
//        let filters = {...this.state.filters};
//        console.log('filters (in state): ', filters);
//
//        // Filters are stored in the state `filters` in the following way:
//        // filters: {
//        //      'publisher': {
//        //          'Publisher 1': true,
//        //          'Publisher 2': true,
//        //          'Publisher 3': true,
//        //      },
//        //      'state': {
//        //          'published': true,
//        //          'rejected': true,
//        //      }
//        // Object way was chosen in order to make it simpler to
//        // add/remove/change.
//        // In the example above, "publisher" and "state" are `filterName`.
//        // "Publisher 1", "Publisher 2", "Publisher 3", "published" and
//        // "rejected" are values (for "publisher" and "state").
//
//        // When we deal with filter which already exists in the state.
//        if (filterName in filters) {
//            console.log('filters[filterName]: ', filters[filterName]);
//            if (filterValue in filters[filterName]) {
//                // If "Publisher 1" was already there and remove is triggered.
//                if (remove) {
//                    let filterOptions = {...filters[filterName]}
//                    delete filterOptions[filterValue];
//                    filters[filterName] = filterOptions;
//                    console.log('setting state 1: ', {filters: filters});
//                    this.setState({filters: filters});
//                }
//            } else {
//                // If "Publisher 1" was already there and now "Publisher 2"
//                // arrives, we simply append "Publisher 2".
//                filters[filterName][filterValue] = true;
//                console.log('setting state 2: ', {filters: filters});
//                this.setState(filters: filters);
//            }
//        } else {
//            if (!remove) {
//                filters[filterName] = {[filterValue]: true};
//                console.log('setting state 3: ', {filters: filters});
//                this.setState({filters: filters});
//            }
//        }
    }

    /**
     * Update all filters.
     */
    updateFilters() {
        let filters = {}
        const formFilters = [].filter.call(document.getElementsByTagName('input'), (c) => c.checked).map(c => [c.name, c.value]);
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
        this.setState({filters: filters});
        return filters;
    }

    onSubmit(event) {
        event.preventDefault();
        this.props.updateQuery(this.state.query);
        this.doSearch();
    }

    onChange(event) {
        event.preventDefault();
        this.setState({
            [event.currentTarget.name]: event.currentTarget.value
        });
    }

    renderResults() {
        const { results, count, query } = this.state;
        return (
            <Fragment>
                {count} hits that match your search criteria: {query}
                {
                    results.map(
                        function(result, index) {
                            return <Result key={index} {...result} />;
                        }
                    )
                }
            </Fragment>
        )
    }

    renderFilters() {
        const { facets } = this.state;
        const doUpdateFilter = this.updateFilter;
        const doSearch = this.doSearch;
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
                                        updateFilter={doUpdateFilter}
                                        doSearch={doSearch}
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

    render() {
        const { updateQuery } = this.props;
        return (
            <Fragment>
                <div className="search-wrapper">
                    <div className="top-wrapper">
                        <h2>Search form</h2>
                        <form onSubmit={this.onSubmit}>
                            <label>Query</label>
                            <input key="query"
                                   name="query"
                                   defaultValue={this.state.query}
                                   onChange={this.onChange} />

                            <button
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
                            <h2>Results</h2>
                            {this.renderResults()}
                        </div>
                    </div>
                </div>

            </Fragment>
        )
    }
}


export default withRouter(Search);
