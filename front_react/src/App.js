import React, { Component } from 'react';
import './App.css';
import Formulario from './components/Formulario/Formulario';



/*------------------------------------------------------------------------------------
* Clase principal. Llama a los datos y muestra la vista
*/
class App extends Component {

    render() {
        return (
            <Formulario/>
        )
    }

}

export default App;
