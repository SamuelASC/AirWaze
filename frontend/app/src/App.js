import './App.css';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import TelaInicial from './components/TelaInicial';
import Login from './components/Login';

function App() {
  return (
    
    <div className="App">
      <Router>
        <Routes>
            <Route path="/"  Component={TelaInicial} />
            <Route path="/Login" Component={Login} />
          </Routes>
      </Router>
      
      
      <header className="App-header">
        <TelaInicial />
      </header>
 
      
    </div>
  );
}

export default App;