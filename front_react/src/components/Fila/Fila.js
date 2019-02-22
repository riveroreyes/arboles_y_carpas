import React from 'react';
import Imagen from '../../components/Imagen/Imagen';

/*------------------------------------------------------------------------------------
* Crea la fila de cada tabla
*/
class Fila extends React.Component { 

  render() {

    var imagenes = [];

    this.props.item.forEach( (elem, index) =>
      imagenes.push(<Imagen key={ this.props.linea.toString() + index.toString()  } dato={elem} />)
    );

    return(
      <tr>
        <td><b> {this.props.row} </b></td>
        {imagenes}
      </tr>
    )
  }
}

export default Fila;