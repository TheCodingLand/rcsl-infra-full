import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import io from 'socket.io-client';
let SOCKET_URL = "uploadws.lbr.lu"
let socket = io.connect(SOCKET_URL);

ReactDOM.render(<App socket={socket} />, document.getElementById('root'));
registerServiceWorker();
