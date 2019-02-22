import React from 'react';

/*------------------------------------------------------------------------------------
* Maneja la configuracion de la imagen
*/
class Imagen extends React.Component {

  render() {

    let imagen = "";
    if(this.props.dato === 1){
      imagen = 'img/grass.png';
    }else if(this.props.dato === 2){
      imagen = 'img/tree.png';
    }else if(this.props.dato === 3){
      imagen = 'img/tent.png';
    }else{
      imagen = 'img/blanco.png';
    }

    return(
      <td> <img src={imagen} alt=""/></td>
    )
  }
}

export default Imagen;
