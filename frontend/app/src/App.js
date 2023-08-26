import './App.css';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import TelaInicial from './components/TelaInicial';
import Login from './components/Login';


function App() {
  return (
    
    <div className="App">
          
      <header className="App-header">
        <TelaInicial />
        <Login />
      </header>
 
      
    </div>
  );
}

export default App;