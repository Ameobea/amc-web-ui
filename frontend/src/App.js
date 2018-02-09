import React, { Component } from "react";
import {
  Button,
  FormControl,
  ControlLabel,
  FormGroup,
  HelpBlock,
} from "react-bootstrap";
import "./App.css";

const FieldGroup = ({ id, label, help, ...props }) => (
  <FormGroup controlId={id}>
    <ControlLabel>{label}</ControlLabel>
    <FormControl {...props} />
    {help && <HelpBlock>{help}</HelpBlock>}
  </FormGroup>
);

class App extends React.Component {
  handleSubmit = () => {
    alert(this.questionNameRef.value);
  }

  render = () => (
    <div style={{ width: 500, marginLeft: 20 }}>
      <form>
        <FieldGroup
          type="text"
          label="Question Name"
          placeholder="Enter text"
          inputRef={ref => this.questionNameRef = ref}
        />
        <Button
          bsStyle="primary"
          onClick={this.handleSubmit}
        >
          Submit
        </Button>
      </form>
    </div>
  );
}

export default App;
