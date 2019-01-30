import React, {Component} from 'react';
import UserCard from './UserCard';
import UserDetail from './UserDetail';
import SearchBar from './SearchBar';
import { connect } from 'react-redux'
import { usersFetchData, userTypesFetchData, incrementPage } from '../redux/actions/users';

//generic modal container
const Modal = ({ children, closeModal, modalState, title }) =>
{
    if(!modalState) {
        return null;
    }

    return(
        <div className="modal is-active">
            <div className="modal-background" onClick={closeModal}/>
            <div className="modal-card">
                <header className="modal-card-head">
                <p className="modal-card-title">{title}</p>
                </header>
                <section className="modal-card-body">
                    <div className="content">
                        {children}
                    </div>
                </section>
            </div>
        </div>
    )
}

class UsersList extends Component {
    constructor  (props) {
        super(props);
        this.handleOnClick = this.handleOnClick.bind(this);

        this.state = {
            modalState: false
        };
        this.toggleModal = this.toggleModal.bind(this);
        this.setCurrentUser = this.setCurrentUser.bind(this);
        this.itemClicked = this.itemClicked.bind(this);
        this.createClicked = this.createClicked.bind(this);
    }

    componentDidMount() {
        this.props.fetchData("?page_size=12");
        this.props.fetchTypes();
        console.log(this.props.users)
        console.log(this.props.types)
    }

    handleOnClick(event) {
        this.props.dispatchIncrementPage();
        const page = this.props.page;
        this.props.fetchData("?page_size=12&page="+page+"&search_term="+this.props.searchText,true);
    }

    setCurrentUser(user)
    {
        this.setState((prev, props) => {
            return { currentUser: user};
        });
    }

    toggleModal()
    {
        this.setState((prev, props) => {
            const newState = !prev.modalState;
            return { modalState: newState };
        });
    }

    itemClicked(index,user)
    {
        //set the current user and toggle the modal
        this.setCurrentUser({index:index,user:user})
        this.toggleModal()
    }

    createClicked()
    {
        this.setState((prev, props) => {
            return { currentUser: undefined};
        });
        this.toggleModal()
    }

    render() {
        if (this.props.hasErrored) {
            return <p>Sorry! There was an error loading the items</p>;
        }

        if (this.props.isLoading) {
            return <p>Loading…</p>;
        }

        return (
            <section className="section">
                <div className="container">
                    <SearchBar createClicked={this.createClicked}></SearchBar>
                </div>
                <div className="container">
                    <section className="section">
                        <div>
                            <div className="columns is-multiline">
                            {
                                this.props.users.map((user,index) => {
                                    return (
                                        <div className="column is-3" key={index}><UserCard user={user} index={index} userSelected={this.itemClicked}></UserCard></div>
                                    )
                                })
                            }
                            </div>
                            <div className="column is-3"><button className="button" onClick={(event) => this.handleOnClick(event)}>More...</button></div>
                        </div>

                        <Modal
                            closeModal={this.toggleModal}
                            modalState={this.state.modalState}
                            types={this.props.types}
                            title="User detail"
                        >
                            <UserDetail user={this.state.currentUser}></UserDetail>
                        </Modal>
                    </section> 
                </div>
            </section>
        )
    }
};

const mapStateToProps = (state) => {
    return {
        users: state.userList.users,
        types: state.userList.types,
        hasErrored: state.userList.hasErrored,
        isLoading: state.userList.isLoading,
        page: state.userList.page,
        searchText: state.searchTerm
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        fetchData: (text,append) => dispatch(usersFetchData(text,append)),
        fetchTypes: () => dispatch(userTypesFetchData()),
        dispatchIncrementPage: () => dispatch(incrementPage())
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(UsersList);