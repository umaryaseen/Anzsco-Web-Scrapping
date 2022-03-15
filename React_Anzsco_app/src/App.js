import {  BrowserRouter, Route , Routes } from 'react-router-dom';
import './App.css';
import AnzscoTable from './components/anzscoTable';
import AnzscoSec from './components/anzsco_sec';
import "bootstrap/js/dist/tooltip"


function App() {
  return (
    
    <BrowserRouter>
      <Routes>
        <Route path = "/"  element = {<AnzscoTable/>} exact  />
        <Route path = "/anzsco_sec"  element = {<AnzscoSec/>} exact  />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
