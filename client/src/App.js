import React from 'react';
import './App.css';
import io from 'socket.io-client';
import GameCanvas from './GameCanvas'

// const BLOCK_SIZE = 30;
// const BLOCK_ROWS = 5;
// const BLOCK_COLUMNS = 12;
//
// const GAME_SPECS = {
//   BLOCK_SIZE : BLOCK_SIZE,
//   BLOCK_ROWS : BLOCK_ROWS,
//   BLOCK_COLUMNS : BLOCK_COLUMNS
// }
var socket = io.connect('http://localhost:5000');

class App extends React.Component {
  constructor(props) {
    super(props);
    this.blockSize = null;
    this.canvasWidth = null;
    this.canvasHeight = null;
    this.rows = null;
    this.columns = null;
    this.blocks = null;
    this.state = {
      loading : true,
    }
    this.handleInitialization = this.handleInitialization.bind(this);
  }

  componentDidMount() {


    socket.on( 'connect', function() {
      socket.emit( 'init', {
        data: 'User Connected'
      })});

    socket.on( 'init_resp', this.handleInitialization );
  }

  handleInitialization(initJson) {
     this.blockSize = initJson['block_size'];
     this.canvasWidth = initJson['pixel_width'];
     this.canvasHeight = initJson['pixel_height'];
     this.rows = initJson['row'];
     this.columns = initJson['columns'];
     this.setState({
       loading : false
     });
   }


  render() {
    // console.log(this.blockSize, "loading: ",this.loading)
    if (this.state.loading) {
      return (
        <div>
          loading
        </div>
      )
    }
    return (
      <div className="App">
        <GameCanvas
          blockSize = {this.blockSize}
          canvasWidth = {this.canvasWidth}
          canvasHeight = {this.canvasHeight}
          rows = {this.rows}
          columns = {this.columns}
          // blocks = {this.blocks}
        />
      </div>
    );
  }
}

export default App;
