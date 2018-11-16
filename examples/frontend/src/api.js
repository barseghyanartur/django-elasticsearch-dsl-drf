import axios from 'axios';

import constants from './constants';

const client = axios.create({
    baseURL: constants.api.url,
    validateStatus: function (status) {
        return status >= 200 && status < 300;
    },
});

export default class api {

    static buildUrl(query, filters={}) {
        let queryList = [];
        queryList.push(`search=${query}`);
        for (var filterName in filters) {
            for (var filterValue in filters[filterName]) {
                queryList.push(`${filterName}=${filterValue}`);
            }
        }
        return queryList.join('&');
    }

    static searchBooks = (query, filters) => {
        console.log('constants: ', constants);
        const params = api.buildUrl(query, filters);
        console.log('params: ', params);
        return client({
            method: 'get',
            url: `${constants.api.booksRoute}?${constants.api.booksRouteParams}${'&'}${params}`,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin',
        });
    }

}