import React, { Fragment } from 'react';

import './Filter.css';


class Filter extends React.Component {

    constructor(props) {
        super(props);
        this.doUpdateFilter = this.doUpdateFilter.bind(this);
    }

    doUpdateFilter(event, filterName, filterValue) {
        const { updateFilter } = this.props;
        const { doSearch } = this.props;
        //updateFilter(filterName, filterValue, !event.target.checked);
        doSearch();
    }

    renderFilter(filterName, options) {
        const doUpdateFilter = this.doUpdateFilter;
        return (
            <Fragment>
                {
                    options.map(
                        function(option, index) {
                            return (
                                <div key={index} className="filter-checkbox">
                                    <input
                                        name={filterName}
                                        defaultValue={option.key}
                                        type="checkbox"
                                        onClick={
                                            (event) => {doUpdateFilter(event, filterName, option.key)}
                                        }

                                    />
                                    <span>{option.key} ({option.doc_count})</span>
                                </div>
                            )
                        }
                    )
                }
            </Fragment>
        )
    }

    render() {
        const filter = {...this.props};
        const filterKeys = Object.keys(filter);
        const filterName = filterKeys[0] == 'doc_count' ? filterKeys[1] : filterKeys[0];
        const options = filter[filterName].buckets;
        return (
            <Fragment>
                <div className="filter-wrapper">
                    <h3>{filterName} ({filter.doc_count})</h3>
                    <span className="options">{this.renderFilter(filterName, options)}</span>
                </div>
            </Fragment>
        )
    }
}


export default Filter;
