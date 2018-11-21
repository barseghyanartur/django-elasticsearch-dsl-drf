import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';

import './Result.css';


class Result extends React.Component {

    renderList(tags) {
        return (
            <Fragment>
                <ul>
                {
                    tags.map(
                        function(tag, index) {
                            return <li key={index}>{tag}</li>;
                        }
                    )
                }
                </ul>
            </Fragment>
        )
    }

    render() {
        const { id, title, state, authors, isbn, summary, tags, globalState } = this.props;
        return (
            <Fragment>
                <div className="result-wrapper">
                    <Link to={`/${id}`} globalState={globalState}>
                        <h3>{title}</h3>
                    </Link>
                    {/*
                    <p>{summary}</p>
                    <span className="tags">{this.renderList(tags)}</span>
                    <span className="authors">{this.renderList(authors)}</span>
                    */}
                </div>
            </Fragment>
        )
    }
}


export default Result;
