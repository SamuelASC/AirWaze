import React, { Component } from 'react';
import { Link, BrowserRouter } from 'react-router-dom';
import logo from '../img/logo.png';

function TelaInicial () {
    return (
        <BrowserRouter>
            <div className="form-wrap">
                <img src={logo} alt="Ícone de usuário" /> 
                <h3>BEM-VINDO</h3>
                <p>Encontre drones próximos a você com apenas alguns cliques!</p>
                <Link className='btn-entrar' to="/Login">Entrar</Link>
            </div>
        </BrowserRouter>
    )
}
export default TelaInicial;