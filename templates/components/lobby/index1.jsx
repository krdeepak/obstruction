import React from 'react';
import ReactDOM from 'react-dom'

// renders out the base component
function render_component(){
    const element = (
    <div>
      <h1>Hello, world!</h1>
      <h2>It is {new Date().toLocaleTimeString()}.</h2>
    </div>
  );
  ReactDOM.render(element, document.getElementById('lobby_component'));
}


render_component()
