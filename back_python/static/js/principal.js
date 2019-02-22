class NameForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        value: '6',
        solo_puzzle: '1'
      };

    this.divStyle = {
      paddingRight: '0px',
      marginRight: '0px'
    };

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  render() {
    return (
      <form onSubmit={this.submit}  method="POST">
        <input type="hidden" name="solo_puzzle" value={this.state.solo_puzzle} />
        <div className="form-group row">
            <label className="col-sm-3 col-form-label">Variable:</label>
            <div className="col-sm-9"  style={this.divStyle}>
                <input type="number" value={this.state.value} onChange={this.handleChange}  name="dimension"  className="form-control" min="6" max="10" />
            </div>
        </div>
        <div className="row">
            <input type="submit" value="Start" className="btn btn-link btn-block" />
        </div>    
      </form>
    );
  }
}

ReactDOM.render(
  <NameForm />,
  document.getElementById('root')
);