import React from 'react';
import './GameCanvas.css';

//edit this to change the game
// const BLOCK_SIZE = 30;
// const BLOCK_ROWS = 5;
// const BLOCK_COLUMNS = 12;

class GameCanvas extends React.Component {
  constructor(props) {
    super(props);
    this.specs = this.props.GAME_SPECS;
    this.state = {
      init : false,
      ctx : null,
    }
  }

  initBoard() {
    this.setState({ctx : {fillStyle : "#FF0000"}});
    console.log(this.state.ctx);
    this.makeBorder();
  }

  makeBorder() {
    // console.log("here");
    for (let blockIndex = 0; blockIndex < this.refs.game_canvas.width / this.specs.BLOCK_SIZE; blockIndex++) {
      //top
      this.state.ctx.fillRect(blockIndex * this.specs.BLOCK_SIZE, 0,
        this.specs.BLOCK_SIZE, this.specs.BLOCK_SIZE);
      //left
      this.state.ctx.fillRect(0, blockIndex * this.specs.BLOCK_SIZE,
        this.specs.BLOCK_SIZE, this.specs.BLOCK_SIZE);
      //right
      this.state.ctx.fillRect(this.refs.game_canvas.width - this.specs.BLOCK_SIZE,
         blockIndex * this.specs.BLOCK_SIZE, this.specs.BLOCK_SIZE, this.specs.BLOCK_SIZE);
    }
  }

  drawBlocks() {

  }

  componentDidMount() {
    if (!this.state.init) {
      this.setState({ctx : this.refs.game_canvas.getContext("2d"),
                     init : true}, function() {
                       this.refs.game_canvas.width = this.specs.BLOCK_SIZE * (this.specs.BLOCK_COLUMNS + 2);
                       this.refs.game_canvas.height = this.specs.BLOCK_SIZE * (this.specs.BLOCK_COLUMNS + 2);
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
