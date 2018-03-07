import React from 'react';
import LobbyBase from './LobbyBase'
import ReactDOM from 'react-dom'
import $ from 'jquery'

// lobby socket url
var lobby_sock = 'ws://' + window.location.host + "/lobby/"
// preset the current_user
var current_user = null

$.get('http://localhost:8000/current-user/?format=json', function(result){
    // gets the current user information from Django
    current_user = result
    render_component()
})

// renders out the base component
function render_component(){
    ReactDOM.render(<LobbyBase current_user={current_user} socket={lobby_sock}/>, document.getElementById('lobby_component'))
}
