import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/tooltip"

import Counter from './components/counter';
import AnzscoTable from './components/anzscoTable';
import AnzscoSec from './components/anzsco_sec';
import {  BrowserRouter, Route , Switch } from 'react-router-dom';

ReactDOM.render(
    <App />, 
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
