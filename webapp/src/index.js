import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';
import './Components/css/mainstyles.css';

import App from './Components/javascript/app';
import reportWebVitals from './Components/javascript/reportWebVitals';

ReactDOM.render(

  <Router>
    <App />
  </Router>,
  document.getElementById('root')
);

reportWebVitals();
