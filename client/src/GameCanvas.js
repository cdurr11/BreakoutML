import React from 'react';
import './GameCanvas.css';

class GameCanvas extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      init : false,
      ctx : null,
    }

  }

  initBoard() {
    this.setState({ctx : {fillStyle : "#FF0000"}});
    console.log(this.state.ctx);
    this.state.ctx.fillRect(0, 0, 20, 20);
  }

  componentDidMount() {
    if (!this.state.init) {
      this.setState({ctx : this.refs.game_canvas.getContext("2d"),
                     init : true}, function() {
                       this.refs.game_canvas.width = 300;
                       this.refs.game_canvas.height = 300;
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
