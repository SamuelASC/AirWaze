import { Router, Route, Routes} from 'react-router-dom';
import TelaInicial from './components/TelaInicial';
import Login from './components/Login';

function MainRoutes() {
    <Router>
        <Routes>
            <Route path="/"  element={<TelaInicial />} />
            <Route path="/Login" element={<Login />} />
        </Routes>
    </Router>
}
export default MainRoutes;
   