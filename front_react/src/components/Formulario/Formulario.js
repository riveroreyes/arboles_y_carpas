import React from 'react';
import Fila from '../../components/Fila/Fila';

class Formulario extends React.Component {

    constructor(props) {
        super(props);

        const dimen = 10;

        this.state = {
            dimension: dimen,
            url: 'http://0.0.0.0:5000/api/procesar_lista',
            resp: [...Array(dimen)].map(x=>Array(dimen).fill(0)),    //new Array(dimen).fill(0).map(() => new Array(dimen).fill(0)),
            cols: [...Array(dimen)].map(x=>0),                       //new Array(dimen),
            rows: [...Array(dimen)].map(x=>0),                       //new Array(dimen),
            cuerpo: [],
            columnas: [],
            filas: []
        };


        this.divStyle = {
            paddingRight: '0px',
            marginRight: '0px'
        };

        this.handleChange = this.handleChange.bind(this);
        this.submit = this.submit.bind(this);
    }

    /*-----------------------------------------------------------------------------------
    * Establece el valor de los estados en base a los vectores resp, cols y rows.
    */
    setEstados(){

        let intIndex = 1000;
        let arr = [];
        let columna = [<th key={intIndex++}></th>];

        this.state.resp.forEach( (item, index) => 
            arr.push(<Fila key={index} item={item} linea={index} row={  this.state.rows[index] } />)
        );

        this.state.cols.forEach( (elem, index) =>
            columna.push(<th key={intIndex++}>{elem}</th>)
        );

        this.setState({
            cuerpo: arr,
            columnas: columna
        });
        
    }

    componentWillMount() {
        this.setEstados();
    }

    handleChange(event) {
        this.setState({dimension: event.target.value});
    }

    submit(e){
        e.preventDefault()

        fetch( this.state.url, {
            method: 'POST',
            headers: {'Content-Type':'application/json'}, 
            body: JSON.stringify( { dimension: parseInt( e.target.dimension.value ) }  )
        
        }).then((response) => {
            return response.json();
        
        }).then((respuesta) => {
            this.setState({ 
                resp: respuesta.resp, 
                cols: respuesta.cols, 
                rows: respuesta.rows
            })

            if (this.state.resp.length > 0) {
                this.setEstados();
            }
        });

    }

    render() {
        return (
            <div className="container">
                <div className="row principal">
                    <table border="1">

                        <thead>
                            <tr>
                            {this.state.columnas}
                            </tr>
                        </thead>

                        <tbody>
                            {this.state.cuerpo}
                        </tbody>

                    </table>
                </div>

                <div className="row principal">
                    <div className="col-12 col-sm-6 col-md-3">
                        <form onSubmit={this.submit}  method="POST">
                            <div className="form-group row">
                                <label className="col-12 col-sm-3 col-form-label">Tamaño:</label>
                                <div className="col-12 col-sm-9"  style={this.divStyle}>
                                    <input type="number" value={this.state.dimension} onChange={this.handleChange}  name="dimension"  className="form-control" min="6" max="200" />
                                </div>
                            </div>
                            <div className="row">
                                <input type="submit" value="Leer y validar" className="btn btn-outline-info btn-block" />
                            </div>    
                        </form>
                    </div>
                </div>

            </div>
        );
    }
}

export default Formulario;
