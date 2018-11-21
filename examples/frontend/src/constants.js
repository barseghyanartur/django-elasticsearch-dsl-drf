const constants = {
  api: {
    url: 'http://localhost:8000', // django-elasticsearch-dsl-drf URL host
    searchRoute: '/search/books-frontend/', // Search route
    searchRouteParams: 'facet=publisher' + // Default search params
                       '&facet=status' +
                       '&facet=price' +
                       '&facet=publication_date',
    rangeFilters: ['price', 'publication_date',],
    searchPageSize: 10,
    suggestionsRoute: '/search/books-frontend/suggest/', // Suggestions route
    suggester: 'title_suggest',
  }
};

export default constants;
