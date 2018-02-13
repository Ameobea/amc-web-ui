import React, { Component } from "react";
import {
  Button,
  FormControl,
  ControlLabel,
  FormGroup,
  HelpBlock,
} from "react-bootstrap";
import "./App.css";
import {AnswerField} from "./answerField.js";

const FieldGroup = ({ id, label, help, ...props }) => (
  <FormGroup controlId={id}>
    <ControlLabel>{label}</ControlLabel>
    <FormControl {...props} />
    {help && <HelpBlock>{help}</HelpBlock>}
  </FormGroup>
);

class App extends React.Component {
  handleSubmit = () => {
    alert(this.questionNameRef.value + this.answer1Ref.value + this.answer2Ref.value + this.answer3Ref.value + this.answer4Ref.value);
  }

  render = () => (
    <div style={{ width: 520, marginLeft: 20 }}>
      <form>
        <FieldGroup
          type="text"
          label="Question Name"
          placeholder="Enter text"
          inputRef={ref => this.questionNameRef = ref}
        />
        <div style={{ width: 500, marginLeft: 20 }}>
          <AnswerField
            type="text"
            label="Answer 1"
            placeholder="Enter text"
          />
          <AnswerField
            type="text"
            label="Answer 2"
            placeholder="Enter text"
            inputRef={ref => this.answer2Ref = ref}
          />
          <AnswerField
            type="text"
            label="Answer 3"
            placeholder="Enter text"
            inputRef={ref => this.answer3Ref = ref}
          />
          <AnswerField
            type="text"
            label="Answer 4"
            placeholder="Enter text"
            inputRef={ref => this.answer4Ref = ref}
          />
          <AnswerField
            type="text"
            label="Answer 5"
            placeholder="Enter text"
            inputRef={ref => this.answer5Ref = ref}
          />
        </div>
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
