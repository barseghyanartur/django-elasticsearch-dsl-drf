import axios from 'axios';

import constants from './constants';

const client = axios.create({
    baseURL: constants.api.url,
    validateStatus: function (status) {
        return status >= 200 && status < 300;
    },
});

export default class api {

    static buildSearchUrl(query, filters={}) {
        let queryList = [];
        queryList.push(`search=${query}`);
        for (var filterName in filters) {
            // Apply additional suffixes for range filters
            let filterSuffix = (constants.api.rangeFilters.indexOf(filterName) > -1) ? '__range' : '';
//            console.log('filterName: ', filterName);
//            console.log('filterSuffix: ', filterSuffix);
            for (var filterValue in filters[filterName]) {
                queryList.push(`${filterName}${filterSuffix}=${filterValue}`);
            }
        }
        return queryList.join('&');
    };

    static search = (query, filters, page=1) => {
        console.log('constants: ', constants);
        const params = api.buildSearchUrl(query, filters);
        console.log('params: ', params);
        return client({
            method: 'get',
            url: `${constants.api.searchRoute}?` +
                 `${constants.api.searchRouteParams}` +
                 `${'&'}page_size=${constants.api.searchPageSize}` +
                 `${'&'}page=${page}` +
                 `${'&'}${params}`,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin',
        });
    };

    static detail = (id) => {
        return client({
            method: 'get',
            url: `${constants.api.searchRoute}${id}/`,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin',
        });
    };

    static suggest = (query, field=constants.api.suggester) => {
        return client({
            method: 'get',
            url: `${constants.api.suggestionsRoute}?${field}=${query}`,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin',
        });
    }
}
