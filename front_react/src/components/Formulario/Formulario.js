import React from 'react';
import Fila from '../../components/Fila/Fila';

class Formulario extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            dimension: '6',
            solo_puzzle: '1',
            resp: [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],
            cols: [0,0,0,0,0,0],
            rows: [0,0,0,0,0,0],
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

        let fila = [];

        this.state.resp.forEach(function(item, index){
            fila.push(<Fila key={index} item={item} linea={index}/>);
        });

        this.setState( {filas: fila} )

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

            console.log(this.state);

            if (this.state.resp.length > 0) {
              
                let fila = [];

                this.state.resp.forEach(function(item, index){
                    fila.push(<Fila key={index} item={item} linea={index}/>);
                });

                this.setState( {filas: fila} )

            } else {
                return <p className="text-center">No fue posible obtener la consulta...</p> 
            }



        })

    }

    render() {
        return (
            <div className="container">
                <div className="row" id="principal">
                    <div className="col-4">
                        <div className="row">
                            <table border="1">
                              <tbody>
                                {this.state.filas}
                              </tbody>
                            </table>
                        </div> 

                    </div>

                    <div className="col-4">

                        <form onSubmit={this.submit}  method="POST">
                            <input type="hidden" name="solo_puzzle" value={this.state.solo_puzzle} />
                            <div className="form-group row">
                                <label className="col-sm-3 col-form-label">Tamaño:</label>
                                <div className="col-sm-9"  style={this.divStyle}>
                                    <input type="number" value={this.state.dimension} onChange={this.handleChange}  name="dimension"  className="form-control" min="6" max="200" />
                                </div>
                            </div>
                            <div className="row">
                                <input type="submit" value="Leer y validar" className="btn btn-primary btn-block" />
                            </div>    
                        </form>

                    </div>

                </div>
            </div>
        );
    }
}

export default Formulario;
