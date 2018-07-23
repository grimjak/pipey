import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import './DynamicForm'
import axios from 'axios';
import {Bootstrap, Grid, Row, Col, FormGroup, FormControl, ControlLabel, HelpBlock} from 'react-bootstrap';

import API from './api'
import DynamicForm from './DynamicForm';

class NewUserForm extends React.Component {
  constructor(props, context) {
    super(props, context)
    this.state = {value:''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    console.log(event.target)
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    alert(('a name was submitted: ' + this.state.value));
    event.preventDefault();
  }

  getValidationState() {
    const length = this.state.value.length;
    if (length > 10) return 'success';
    else if (length > 5) return 'warning';
    else if (length > 0) return 'error';
    return null;
  }


  render() {

    function FieldGroup({ id, label, help, ...props }) {
      return (
        <FormGroup controlId={id}>
          <ControlLabel>{label}</ControlLabel>
          <FormControl {...props} />
          {help && <HelpBlock>{help}</HelpBlock>}
        </FormGroup>
      );
    }

    return (
      <form>
        <FormGroup
          controlId="formBasicText"
          validationState={this.getValidationState()}
        >
          <FieldGroup
            id="formControlsText"
            type="text"
            label="Text"
            placeholder="Enter text"
            onChange={this.handleChange}
          />
          <ControlLabel>Working example with validation</ControlLabel>
          <FormControl
            type="text"
            value={this.state.value}
            placeholder="Enter text"
            onChange={this.handleChange}
          />
          <FormControl.Feedback />
          <HelpBlock>Validation is based on string length.</HelpBlock>
        </FormGroup>
      </form>
    );
  }
}


class App extends Component {
  state = {
    people: [1,2,3],
  };

  componentDidMount() {
    console.log("componeneDidMount");
    API.get(`/people`)
      .then(res => this.setState({ people: res.data }))
      .catch(err => console.log(err)); 
    console.log(this.state.people);
  }
  render() {
    console.log(this.state.people);
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <ul className="App-intro">
          <DynamicForm className="form"
            title = "New user"
            model = {[
              {key:"name", label: "Forename", props: {required: true}},
              {key:"surname", label: "Surname", props: {required: true}}
            ]}
            onSubmit = {(model)=>{this.onSubmit(model)}}
          />
        </ul>
      </div>
    );
  }
}

export default App;
