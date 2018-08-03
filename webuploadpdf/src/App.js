import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Upload from './components/Upload'
import Step from './components/Step'
import io from 'socket.io-client';



class App extends Component {
  constructor() {
    super()
    let SOCKET_URL = "uploadws.lbr.lu"
    let socket = io.connect(SOCKET_URL)
    this.state = {
      socket: socket,
      connected:false
    }
    
    this.state.socket.on('connect', this.setConnected)

      
    this.state.socket.on('disconnect',this.setDisconnected)
    //{ this.setState({connected : false})}).bind(this);


  }
  setConnected = () => { this.setState({connected : true})
    console.log('setting connected') } 
    setDisconnected = () => {  
      this.setState({connected : false})}

  render() {
    return (
      <div className="App">
     
      
          <Step step={1}/>
          {this.state.socket.connected ==true ? <Upload socket={this.state.socket}/> : <p>loading socket</p>}
          
      </div>
    );
  }
}

export default App;
