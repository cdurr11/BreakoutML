import React from 'react';
import './GameCanvas.css';
import io from 'socket.io-client';
//edit this to change the game
// const BLOCK_SIZE = 30;
// const BLOCK_ROWS = 5;
// const BLOCK_COLUMNS = 12;
var socket = io.connect('http://localhost:5000');
let ctx;

class GameCanvas extends React.Component {

  constructor(props) {
    super(props);
    this.specs = this.props.GAME_SPECS;
    this.state = {
      init : false,
      ctx : null,
    }
    this.redrawCanvas = this.redrawCanvas.bind(this);

  }

  initBoard() {
    // this.setState({ctx : {fillStyle : "#FF0000"}});
    // console.log(this.state.ctx);
    // this.setState(prevState => ({
    //   ctx : {
    //     ...prevState.ctx,
    //     fillStyle : "#FF0000"
    //   }
    // }));
    // console.log(this.state.ctx);
    // this.makeBorder();
  }

  makeBorder() {
    // console.log(this.props.blocks);
    // // console.log("here");
    // for (let blockIndex = 0; blockIndex < this.refs.game_canvas.width / this.props.blockSize; blockIndex++) {
    //   //top
    //   this.state.ctx.fillRect(blockIndex * this.props.blockSize, 0,
    //     this.props.blockSize, this.props.blockSize);
    //   //left
    //   this.state.ctx.fillRect(0, blockIndex * this.props.blockSize,
    //     this.props.blockSize, this.props.blockSize);
    //   //right
    //   this.state.ctx.fillRect(this.refs.game_canvas.width - this.props.blockSize,
    //      blockIndex * this.props.blockSize, this.props.blockSize, this.props.blockSize);
    // }
  }


  drawBlocks() {

  }
  redrawCanvas(json) {
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
    // console.log("redrawing", json);
  }

  componentDidMount() {
    socket.emit( 'start_play', {});
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
