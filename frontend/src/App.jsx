// src/App.jsx
import React from 'react';
import CreateAccount from './components/CreateAccount';
import Login from './components/Login';
import ChatWindow from './components/ChatWindow';

function App() {
  return (
    <div className="App">
      <CreateAccount />
      <Login />
      <ChatWindow />
    </div>
  );
}

export default App;
