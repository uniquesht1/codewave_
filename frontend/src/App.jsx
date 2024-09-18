// src/App.jsx
import React from 'react';
import { Outlet } from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <Outlet /> {/* This will render child routes */}
    </div>
  );
}

export default App;
