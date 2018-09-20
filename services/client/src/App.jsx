import React, { Component } from 'react';
import axios from 'axios';

import UsersList from './components/UsersList';
import AddUser from './components/AddUser';
import About from './components/About';
import NavBar from './components/NavBar';

import { Route, Switch } from 'react-router-dom';
import Form from './components/Form';
import Logout from './components/Logout';

class App extends Component {
    constructor() {
        super();
        this.state = {
            users: [],
            username:'',
            firstname: '',
            lastname:'',
            address:'',
            title: 'TestDriven.io',
            formData: {
                username:'',
                password:''
            },
            isAuthenticated: false,
        };
        this.addUser = this.addUser.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
        this.handleFormChange = this.handleFormChange.bind(this);
        this.logoutUser = this.logoutUser.bind(this);
    };
    componentDidMount() {
        this.getUsers();
    };
    getUsers() {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/api/people`)
        .then((res) => { this.setState({ users: res.data }); })
        .catch((err) => { console.log(err); });
    }
    addUser(event) {
        event.preventDefault();
        const data = {
            username: this.state.username,
            firstname: this.state.firstname,
            lastname: this.state.lastname,
            address: this.state.address
        };
        axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/api/people`, data)
            .then((res) => {
                this.getUsers();
                this.setState({username: '', firstname: '', lastname: '', address: ''});
            })
            .catch((err) => {console.log(err)});
    };
    handleChange(event) {
        const obj = {};
        obj[event.target.name] = event.target.value;
        this.setState(obj);
    };
    handleUserFormSubmit(event) {
        event.preventDefault();
        const formType = window.location.href.split('/').reverse()[0];
        let data = {
            username: this.state.formData.username,
            password: this.state.formData.password,
        };
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`
        axios.post(url, data)
        .then((res) => {
            this.clearFormState();
            window.localStorage.setItem('authToken', res.data.auth_token);
            this.setState({ isAuthenticated: true});
            this.getUsers();
        })
        .catch((err) => { console.log(err); });
    }
    handleFormChange(event) {
        const obj = this.state.formData;
        obj[event.target.name] = event.target.value;
        this.setState(obj);
    }
    clearFormState() {
        this.setState({
            formData: { username: '', password: '' },
            username: '',
            password: '',
        });
    };
    logoutUser(){
        window.localStorage.clear();
        this.setState({ isAuthenticated: false});
    };
    render() {
        return (
            <div>
                <NavBar title={this.state.title} />
                <section className="section">
                    <div className="container">
                        <div className="columns">
                            <div className="column is-half">
                            <Switch>
                                <Route exact path='/' render={() => (
                                <div>
                                    <h1 className="title is-1">All Users</h1>
                                    <hr/><br/>
                                    <AddUser
                                        username={this.state.username}
                                        firstname={this.state.firstname}
                                        lastname={this.state.lastname}
                                        address={this.state.address}
                                        addUser={this.addUser}
                                        handleChange={this.handleChange}
                                    />
                                    <br/><br/>
                                    <UsersList users={this.state.users}/>
                                </div>
                                )} />
                                <Route exact path='/about' component={About}/>
                                <Route exact path='/login' render={() => (
                                    <Form
                                        formType={'Login'}
                                        formData={this.state.formData}
                                        handleFormChange={this.handleFormChange}
                                        handleUserFormSubmit={this.handleUserFormSubmit}
                                        isAuthenticated={this.state.isAuthenticated}
                                    />
                                )} />
                                <Route exact path='/logout' render={() => (
                                    <Logout
                                        logoutUser={this.logoutUser}
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