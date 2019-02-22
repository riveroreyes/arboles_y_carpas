class NameForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '16',
      solo_puzzle: '1'
    };

    this.divStyle = {
      paddingRight: '0px',
      marginRight: '0px'
    };

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  render() {
    return React.createElement(
      'form',
      { onSubmit: this.submit, method: 'POST' },
      React.createElement('input', { type: 'hidden', name: 'solo_puzzle', value: this.state.solo_puzzle }),
      React.createElement(
        'div',
        { className: 'form-group row' },
        React.createElement(
          'label',
          { className: 'col-sm-3 col-form-label' },
          'Tamaño'
        ),
        React.createElement(
          'div',
          { className: 'col-sm-9', style: this.divStyle },
          React.createElement('input', { type: 'number', value: this.state.value, onChange: this.handleChange, name: 'dimension', className: 'form-control', min: '6', max: '200' })
        )
      ),
      React.createElement(
        'div',
        { className: 'row' },
        React.createElement('input', { type: 'submit', value: 'Leer y Validar', className: 'btn btn-primary btn-block' })
      )
    );
  }
}

ReactDOM.render(React.createElement(NameForm, null), document.getElementById('root'));
