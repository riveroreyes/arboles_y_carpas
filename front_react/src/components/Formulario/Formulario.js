import React from 'react';
import Fila from '../../components/Fila/Fila';

class Formulario extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            dimension: '10',
            solo_puzzle: '1',
            resp: [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]],
            cols: [0,0,0,0,0,0,0,0,0,0],
            rows: [0,0,0,0,0,0,0,0,0,0],
            items: [],
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

    componentWillMount() {

        let intIndex = 1000;
        let arr = [];
        let columna = [<th key={intIndex++}></th>];
        var dato = this.state.rows;

        this.state.resp.forEach( function(item, index){
            arr.push(<Fila key={index} item={item} linea={index} row={dato[index]} />);
        });

        this.state.cols.forEach(function(elem, index){
            columna.push(<th key={intIndex++}>{elem}</th>);
        });

        this.setState( {
            items: arr,
            columnas: columna
        } )

    }

    handleChange(event) {
        this.setState({dimension: event.target.value});
    }

    submit(e){
        e.preventDefault()

        var data = {
            dimension: parseInt( e.target.dimension.value )
        }

        fetch('http://0.0.0.0:5000/api/procesar_lista', {
            method: 'POST',
            headers: {'Content-Type':'application/json'}, 
            body: JSON.stringify(data)
        
        }).then((response) => {
            return response.json()
        
        }).then((respuesta) => {
            this.setState({ 
                resp: respuesta.resp, 
                cols: respuesta.cols, 
                rows: respuesta.rows
            })

            if (this.state.resp.length > 0) {
              
                let arr = [];
                let dato = this.state.rows;

                this.state.resp.forEach(function(item, index){
                    arr.push(<Fila key={index} item={item} linea={index}  row={dato[index]} />);
                });

                let intIndex = 1000;
                let columna = [<th key={intIndex++}></th>];

                console.log(this.state.cols);

                this.state.cols.forEach(function(elem, index){
                    columna.push(<th key={intIndex++}>{elem}</th>);
                });

                this.setState( {
                    items: arr,
                    columnas: columna
                })

            } else {
                return <p className="text-center">No fue posible obtener la consulta...</p> 
            }



        })

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
                            {this.state.items}
                        </tbody>
                    </table>
                </div>

                <div className="row principal">
                    <div className="col-12 col-sm-6 col-md-3">
                        <form onSubmit={this.submit}  method="POST">
                            <input type="hidden" name="solo_puzzle" value={this.state.solo_puzzle} />
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
