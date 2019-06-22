import React from 'react';
import './App.css';
import io from 'socket.io-client';
import GameCanvas from './GameCanvas'

const BLOCK_SIZE = 30;
const BLOCK_ROWS = 5;
const BLOCK_COLUMNS = 12;

const GAME_SPECS = {
  BLOCK_SIZE : BLOCK_SIZE,
  BLOCK_ROWS : BLOCK_ROWS,
  BLOCK_COLUMNS : BLOCK_COLUMNS
}

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
        <GameCanvas GAME_SPECS = {GAME_SPECS}/>
      </div>
    );
  }
}

export default App;
