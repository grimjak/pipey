import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';

import App from './App.jsx';
import { Provider } from 'react-redux';
import configureStore from './redux/store';

import 'bulma/css/bulma.min.css'
import '@fortawesome/fontawesome-free/css/all.min.css'


const store = configureStore();

ReactDOM.render((
    <Router>
        <Provider store={store}>
            <App />
        </Provider>
    </Router>
    ), document.getElementById('root'))
