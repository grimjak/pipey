import React, {Component} from 'react';
import { connect } from 'react-redux'
import { usersFetchData } from '../redux/actions/users';
import { searchTermModified } from '../redux/actions/search';

class SearchBar extends Component {
    constructor  (props) {
        super(props);
        this.handleFormChange = this.handleFormChange.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
    }
    handleFormChange(event){
       this.props.dispatchSearchTermModified(event.target.value)
       this.props.fetchData("?page_size=12&page="+this.props.page+"&search_term="+this.props.searchText); //Should we be fetching from here? do we need to reset page
    }
    handleFormSubmit(event){
        event.preventDefault();
        this.props.fetchData("?page_size=12&page="+this.props.page+"&search_term="+this.props.searchText); //Should we be fetching from here? do we need to reset page
    }
    render() {
        return (
            <nav className="level">
                <div className="level-left">
                    <div className="level-item">
                        <p className="subtitle is-5">
                            <strong>123</strong> posts
                        </p>
                    </div> 
                    <div className="level-item">
                        <div className="field has-addons" onSubmit={this.handleFormSubmit}>
                            <div className="control is-expanded">
                                <input className="input" type="text" placeholder="Find a user" onChange={this.handleFormChange}></input>
                            </div>
                            <div className="control">
                                <button className="button">
                                    Search
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="level-right">
                    <div className="level-item">
                        <button className="button" onClick={(event) => {this.props.createClicked()}}>Create User</button>
                    </div>
                </div>
            </nav>
        )
    };
};

const mapStateToProps = (state) => {
    return {
        searchText: state.searchTerm,
        page: state.userList.page
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        fetchData: (text) => dispatch(usersFetchData(text)),
        dispatchSearchTermModified: (text) => dispatch(searchTermModified(text))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(SearchBar);