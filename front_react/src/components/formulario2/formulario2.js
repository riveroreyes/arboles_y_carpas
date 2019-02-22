import React from 'react';
//import Fila from '../../components/Fila/Fila';

import Config from "../../config/config";

class Formulario extends React.Component {
    constructor(props) {
        super(props);

        const dimen = 10;
        this.state = {
            dimension: dimen,
            resp: [...Array(dimen)].map(x=>Array(dimen).fill(0)),    //new Array(dimen).fill(0).map(() => new Array(dimen).fill(0)),
            cols: [...Array(dimen)].map(x=>0),                       //new Array(dimen),
            rows: [...Array(dimen)].map(x=>0),                       //new Array(dimen),
        };

        this.divStyle = {
            paddingRight: '0px',
            marginRight: '0px'
        };
    }

    handleChange(event) {
        this.setState({dimension: event.target.value});
    }

    submit(e) {
        e.preventDefault()

        fetch( Config.url, {
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
        });
    }

    onClickCell(i, j) {
    	console.log(i, j);
    }

    render() {
        return (
            <div className="container">
                <div className="row principal">
                    <table border="1">
                        <tbody>
                            <tr>
                            	<td>&nbsp;</td>
                            	{this.state.cols.map((elem, index) => <td key={index}>{elem}</td>)}
                            </tr>
                            {this.state.resp.map((elem, j) => {
                            	return (<tr key={j}>
                            			<td>{this.state.rows[j]}</td>
                            			{elem.map((elem, i) => {
                            				return (
                            					<td 
                            						key={i} 
                            						onClick={() => this.onClickCell(i, j)}>
                            						<span>{this.renderImage(elem)}</span>
                            					</td>
                            				);
                            			} )}
                            		</tr>);
                            })}
                        </tbody>
                    </table>
                </div>

                <div className="row principal">
                    <div className="col-12 col-sm-6 col-md-3">
                        <form onSubmit={(e) => this.submit(e)}  method="POST">
                            <div className="form-group row">
                                <label className="col-12 col-sm-3 col-form-label">Tamaño:</label>
                                <div className="col-12 col-sm-9"  style={this.divStyle}>
                                    <input 
                                    	type="number" 
                                    	value={this.state.dimension} 
                                    	onChange={(e) => this.handleChange(e)}  
                                    	name="dimension"  
                                    	className="form-control" 
                                    	min="6" 
                                    	max="200" />
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

    renderImage(elem) {
	    let imagen = "";
	    if(elem === 1){
	      imagen = 'img/grass.png';
	    }else if(elem === 2){
	      imagen = 'img/tree.png';
	    }else if(elem === 3){
	      imagen = 'img/tent.png';
	    }else{
	      imagen = 'img/blanco.png';
	    }

	    return <img src={imagen} alt="" />;
    }
}

export default Formulario;
