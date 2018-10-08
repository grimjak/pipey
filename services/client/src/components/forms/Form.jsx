import React, { Component } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';
import { loginFormRules } from './form-rules.js';
import FormErrors from './FormErrors.jsx';

class Form extends Component {
    constructor (props) {
        super(props);
        this.state= {
            formData: {
                username: '',
                password: '',
            },
            loginFormRules: loginFormRules,
            valid: false,
        };
        this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
        this.handleFormChange = this.handleFormChange.bind(this);
    };
    componentDidMount() {
        this.clearForm();
        this.validateForm();
    };
    componentWillReceiveProps(nextProps) {
        if (this.props.formType !== nextProps.formType) {
            this.clearForm();
            this.validateForm();
        };
    };
    clearForm() {
        this.setState({
            formData: {username: '', password: ''}
        });
    };
    handleFormChange(event){
        const obj = this.state.formData;
        obj[event.target.name] = event.target.value;
        this.setState(obj);
        this.validateForm();
    };
    handleUserFormSubmit(event){
        event.preventDefault();
        const formType = this.props.formType;
        const data = {
            username: this.state.formData.username,
            password: this.state.formData.password
        };
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`
        axios.post(url, data)
        .then((res) => {
            this.clearForm();
            this.props.loginUser(res.data.auth_token);
        })
        .catch((err) => {
            console.log("error");
            this.props.createMessage('User does not exist.', 'danger'); 
        });
    };
    validateForm() {
        const self = this;
        const formData = this.state.formData;
        self.resetRules();
        //validate rules here
        if (self.props.formType === 'login') {
            const formRules = self.state.loginFormRules;
            if (formData.username.length > 0) formRules[0].valid = true;
            if (formData.password.length > 0) formRules[1].valid = true;
            self.setState({loginFormRules: formRules});
            if (self.allTrue()) self.setState({valid: true});
        }
    };
    allTrue() {
        let formRules = loginFormRules;
        for (const rule of formRules) {
            if (!rule.valid) return false;
        }
        return true;
    };
    resetRules() {
        const loginFormRules = this.state.loginFormRules;
        for (const rule of loginFormRules) {
            rule.valid = false;
        }
        this.setState({loginFormRules: loginFormRules});
        this.setState({valid: false})
    };
    render() {
        if(this.props.isAuthenticated) {
            return <Redirect to='/' />;
        };
        let formRules = this.state.loginFormRules;
        return (
            <div>
                <h1 className="title is-1">{this.props.formType}</h1>
                <hr/><br/>
                <FormErrors
                    formType={this.props.formType}
                    formRules={formRules}
                />
                <form onSubmit={(event) => this.handleUserFormSubmit(event)}>
                    <div className="field">
                        <input
                            name="username"
                            className="input is-medium"
                            type="text"
                            placeholder="Enter username"
                            required
                            value={this.state.formData.username}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    <div className="field">
                        <input
                            name="password"
                            className="input is-medium"
                            type="password"
                            placeholder="Enter password"
                            required
                            value={this.state.formData.password}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    <input
                        type="submit"
                        className="button btn-primary btn-lg btn-block"
                        value="Submit"
                        disabled={!this.state.valid}
                    />
                </form>
            </div>
        )
    };
};

export default Form;