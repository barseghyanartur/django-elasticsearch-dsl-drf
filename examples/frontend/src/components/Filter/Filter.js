import React, { Fragment } from 'react';

import constants from '../../constants';

import './Filter.css';


class Filter extends React.Component {

    constructor(props) {
        super(props);
        this.doUpdateFilter = this.doUpdateFilter.bind(this);
    }

    doUpdateFilter(event, filterName, filterValue) {
        const { doSearch, resetPageNumber } = this.props;
        resetPageNumber();
        doSearch(1); // Always reset to page 1 when updating the filter
    }

    renderFilter(filterName, options) {
        const doUpdateFilter = this.doUpdateFilter;
        const inputType = (constants.api.rangeFilters.indexOf(filterName) > -1) ? 'radio' : 'checkbox';
        return (
            <Fragment>
                {(inputType === 'radio') &&
                    <div key={-1} className="filter-checkbox">
                        <label>
                            <input
                                name={filterName}
                                defaultValue=""
                                type={inputType}
                                onClick={
                                    (event) => {doUpdateFilter(event, filterName, "")}
                                }
                            />
                            <span className="checkable">all</span>
                        </label>
                    </div>
                }
                {
                    options.map(
                        function(option, index) {
                            let optionRepr = option.key;
                            let optionKey = option.key;
                            if ('key_as_string' in option) {
                                // We most likely deal with DateRange facet
                                // of Elasticsearch. We want to parse weird
                                // date representation to a nice (more human
                                // readable) format. Apart from that, we
                                // use range filter (see the `api` part for
                                // that) and thus we need to provide range
                                // values for this case, having casted it
                                // into year format. That why we add `||/y`
                                // ad the end.
                                optionRepr = new Date(option.key_as_string).getFullYear();
                                optionKey = `${option.key_as_string}${'||/y'}__${option.key_as_string}${'||/y'}`;
                            } else if ('to' in option && 'from' in option) {
                                // We most likely deal with Range facet of
                                // Elasticsearch. We want to have a nice
                                // value for it, so we simply use `from` and
                                // `to` fields for that, combining them with
                                // a dash and spaces.
                                optionRepr = `${option.from} - ${option.to}`;
                            }
                            // Remove the `option.doc_count > 0 &&` part from
                            // the next line if you want to have null results
                            // options as well.
                            return (option.doc_count > 0 &&
                                <div key={index} className="filter-checkbox">
                                    <label>
                                        <input
                                            name={filterName}
                                            defaultValue={optionKey}
                                            type={inputType}
                                            onClick={
                                                (event) => {doUpdateFilter(event, filterName, optionKey)}
                                            }
                                        />
                                        <span className="checkable">{optionRepr} ({option.doc_count})</span>
                                    </label>
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
        const filterName = filterKeys[0] === 'doc_count' ? filterKeys[1] : filterKeys[0];
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
