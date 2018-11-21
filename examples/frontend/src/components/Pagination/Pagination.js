import React, { Fragment } from 'react';

import './Pagination.css';


class Pagination extends React.Component {

    render() {
        const { count, pageSize, updatePageNumber, currentPage } = this.props;
        const pages = Math.ceil(count / pageSize);
        return (
            <Fragment>
                <div className="pagination-wrapper">
                {[...Array(pages).keys()].map(p => {
                    const page = p + 1;
                    if (currentPage === page) {
                        return (
                            <strong>{page}</strong>
                        );
                    } else {
                        return (
                            <a href="" onClick={(event) => {
                                event.preventDefault();
                                updatePageNumber(page)
                            }}>
                                {page}
                            </a>
                        );
                    }
                })}
                </div>
            </Fragment>
        );
    }
}


export default Pagination;
