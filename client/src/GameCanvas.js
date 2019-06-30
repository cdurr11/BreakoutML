import React from 'react';
import './GameCanvas.css';
import io from 'socket.io-client';
//edit this to change the game
// const BLOCK_SIZE = 30;
// const BLOCK_ROWS = 5;
// const BLOCK_COLUMNS = 12;
const ARROW_RIGHT = 39;
const ARROW_LEFT = 37;
const PADDLE_HEIGHT = 10;
var socket = io.connect('http://localhost:5000');
let ctx;

class GameCanvas extends React.Component {

  constructor(props) {
    super(props);
    this.specs = this.props.GAME_SPECS;
    this.state = {
      init : false,
      ctx : null,
      leftPressed : false,
      rightPressed : false,
    }
    this.redrawCanvas = this.redrawCanvas.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.handleKeyUp = this.handleKeyUp.bind(this);

  }

  initBoard() {

  }

  makeBorder() {
  }


  drawBlocks() {

  }
  redrawCanvas(json) {
    console.log(json);
    ctx.fillStyle = '#DCDCDC';
    ctx.fillRect(0,0, this.props.canvasWidth, this.props.canvasHeight)
    // console.log(this.state.ctx)
    // this.state.ctx.fillRect(0, 0, this.props.blockSize, this.props.blockSize)
    json['blocks'].forEach((block) => {
      if (block['type'] === "HARD"){
          ctx.fillStyle = 'black';
      }
      else {
        ctx.fillStyle = 'blue';
      }

      ctx.fillRect(block['x'], block['y'], this.props.blockSize, this.props.blockSize)
    }, this);
    ctx.fillRect(json['paddle']['x'], json['paddle']['y'], json['paddle']['width'], PADDLE_HEIGHT);

    socket.emit('start_play',
    {'left' : this.state.leftPressed, 'right' : this.state.rightPressed})
    // console.log("redrawing", json);
  }

  handleKeyDown(event) {
    if ( event.keyCode === ARROW_LEFT ) {
      this.setState({leftPressed : true});
    }
    else if (event.keyCode === ARROW_RIGHT) {
      this.setState({rightPressed  : true});
    }
  }

  handleKeyUp(event) {
    if ( event.keyCode === ARROW_LEFT ) {
      this.setState({leftPressed : false});
    }
    else if (event.keyCode === ARROW_RIGHT) {
      this.setState({rightPressed  : false});
    }
  }

  componentDidMount() {
    document.addEventListener("keydown", this.handleKeyDown);
    document.addEventListener("keyup", this.handleKeyUp);
    socket.emit( 'start_play', {'left' : false, 'right' : false});
    socket.on( 'step', this.redrawCanvas);
    ctx = this.refs.game_canvas.getContext("2d")
    if (!this.state.init) {
      this.setState({
                     init : true}, function() {
                       this.refs.game_canvas.width = this.props.canvasWidth;
                       this.refs.game_canvas.height = this.props.canvasHeight;
                       this.initBoard();
                     });
    }
  }

  render() {
    return (
      <canvas ref="game_canvas" className = "elem--canvas">
      </canvas>
    );
  }
}

export default GameCanvas;
