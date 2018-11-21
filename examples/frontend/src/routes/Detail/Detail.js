import React, { Fragment } from 'react';
import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';

import api from '../../api';
import './Detail.css';


class Detail extends React.Component {

    static propTypes = {
        history: PropTypes.object,
    };

    constructor(props) {
        super(props);
        const { id } = this.props.match.params;
        this.state = {
            id: id,
            title: '',
            description: '',
            summary: '',
            authors: '',
            publisher: '',
            publication_date: '',
            state: '',
            isbn: '',
            price: '',
            pages: '',
            stock_count: '',
            tags: '',
            highlight: '',
            null_field: '',
            score: '',
        };
        this.getResult = this.getResult.bind(this);
        this.componentDidMount = this.componentDidMount.bind(this);
    }

    componentDidMount() {
        console.log('this.props: ', this.props);
        const { id } = this.props.match.params;
        if (id) {
            this.getResult();
        }
    }

    getResult() {
        const { id } = this.state;
        if (id) {
            api.detail(id)
               .then((result) => {
                   this.setState(result.data);
               });
        }
    }

    render() {
        const {
            title,
            description,
            summary,
            authors,
            publisher,
            publication_date,
            state,
            isbn,
            price,
            pages,
            stock_count,
            tags,
            highlight,
            score,
        } = this.state;
        return (
            <Fragment>
                <div className="detail-wrapper">
                    <h1>{title}</h1>
                    <p>{description}</p>
                    <p>{summary}</p>
                    <p>{authors}</p>
                    <p>{publisher}</p>
                    <p>{publication_date}</p>
                    <p>{state}</p>
                    <p>{isbn}</p>
                    <p>{price}</p>
                    <p>{pages}</p>
                    <p>{stock_count}</p>
                    <p>{tags}</p>
                </div>
            </Fragment>
        )
    }
}


export default withRouter(Detail);
