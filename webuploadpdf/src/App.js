import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Upload from './components/Upload'
import Step from './components/Step'


class App extends Component {
  render() {
    return (
      <div className="App">
     
      
          <Step step={1}/>
          <Upload socket = {this.props.socket}/>
          
      </div>
    );
  }
}

export default App;
