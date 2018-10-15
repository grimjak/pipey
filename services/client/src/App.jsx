import React, { Component } from 'react';
import axios from 'axios';

import UsersList from './components/UsersList';
import About from './components/About';
import NavBar from './components/NavBar';

import { Route, Switch } from 'react-router-dom';
import Form from './components/forms/Form';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';
import Message from './components/Message';

class App extends Component {
    constructor() {
        super();
        this.state = {
            users: [],
            title: 'TestDriven.io',
            isAuthenticated: false,
            messageName: null,
            messageType: null,
        };
        this.logoutUser = this.logoutUser.bind(this);
        this.loginUser = this.loginUser.bind(this);
        this.createMessage = this.createMessage.bind(this);
        this.removeMessage = this.removeMessage.bind(this);
    };
    componentWillMount() {
        if (window.localStorage.getItem('authToken')) {
            this.setState({ isAuthenticated: true});
        }
    }
    componentDidMount() {
        this.getUsers();
    };
    getUsers() {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/api/people`)
        .then((res) => { this.setState({ users: res.data }); })
        .catch((err) => { });
    }
    logoutUser(){
        window.localStorage.clear();
        this.setState({ isAuthenticated: false});
    };
    loginUser(token){
        window.localStorage.setItem('authToken', token);
        this.setState({ isAuthenticated: true});
        this.getUsers();
        this.createMessage('Welcome!', 'success');
    };
    createMessage(name='Sanity Check', type='success') {
        this.setState({
            messageName: name,
            messageType: type
        });
        setTimeout(() => {
            this.removeMessage();
        }, 3000);
    };
    removeMessage() {
        this.setState({
            messageName: null,
            messageType: null
        });
    };
    render() {
        return (
            <div>
                <NavBar 
                    title={this.state.title}
                    isAuthenticated={this.state.isAuthenticated}
                />
                <section className="section">
                    <div className="container">
                        {this.state.messageName && this.state.messageType && 
                            <Message
                                messageName={this.state.messageName}
                                messageType={this.state.messageType}
                                removeMessage={this.removeMessage}
                            />
                        }
                        <div className="columns">
                            <div className="column is-half">
                            <Switch>
                                <Route exact path='/' render={() => (
                                <div>
                                    <UsersList 
                                        users={this.state.users}
                                    />
                                </div>
                                )} />
                                <Route exact path='/about' component={About}/>
                                <Route exact path='/login' render={() => (
                                    <Form
                                        formType={'login'}
                                        loginUser={this.loginUser}
                                        isAuthenticated={this.state.isAuthenticated}
                                        createMessage={this.createMessage}
                                        removeMessage={this.removeMessage}
                                    />
                                )} />
                                <Route exact path='/logout' render={() => (
                                    <Logout
                                        logoutUser={this.logoutUser}
                                        isAuthenticated={this.state.isAuthenticated} 
                                    />
                                )} />     
                                <Route exact path='/status' render={() => (
                                    <UserStatus
                                        isAuthenticated={this.state.isAuthenticated}
                                    />
                                )} />                                                              
                                </Switch>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        )
    }
};  

export default App;