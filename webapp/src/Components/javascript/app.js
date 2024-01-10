import React, { Component } from 'react';
import Routes from './router';

import 'bootstrap/dist/css/bootstrap.min.css';

class App extends Component {
  render() {
    // This will send the page to router
    return (
      <div className="App">
        <Routes />
      </div>
    )
  }
}

export default App
