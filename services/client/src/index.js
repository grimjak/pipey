import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';

import App from './App.jsx';

import 'bulma/css/bulma.min.css'

ReactDOM.render((
    <Router>
        <App />
    </Router>
    ), document.getElementById('root'))
