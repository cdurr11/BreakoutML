import React from 'react';
import './App.css';
import io from 'socket.io-client';
import GameCanvas from './GameCanvas'

class App extends React.Component {
  constructor(props) {
    super(props);
    var socket = io.connect('http://localhost:5000');
    socket.on( 'connect', function() {
      socket.emit( 'my event', {
        data: 'User Connected'
      })})

    socket.on( 'my response', function( msg ) {
       console.log( msg )
        })
  }
  render() {
    return (
      <div className="App">
        <GameCanvas/>
      </div>
    );
  }
}

export default App;
