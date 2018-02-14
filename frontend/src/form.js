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
import "./answerField.css";

const FieldGroup = ({ id, label, help, ...props }) => (
  <FormGroup controlId={id}>
    <ControlLabel>{label}</ControlLabel>
    <FormControl {...props} />
    {help && <HelpBlock>{help}</HelpBlock>}
  </FormGroup>
);

export class Form extends React.Component
{
  constructor(props)
  {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.state = {question: '', answer1: '', answer2: '', answer3: '', answer4: '', answer5: ''};
  }
  handleChange(e)
  {
    this.setState({ [e.target.name]: e.target.value });
  }

  handleSubmit = () => {
    //alert(this.answer2Ref.value);
    //this.setState({question: this.questionRef.value});
    alert(JSON.stringify(this.state));
  }

  render()
  {
    return(
    <div style={{ width: 520, marginLeft: 20 }}>
      <form>
        <FieldGroup
          type="text"
          label="Question Name"
          placeholder="Enter text"
          name = 'question'
          value = {this.state.question}
          onChange = {this.handleChange}
        />
        <div style={{ width: 500, marginLeft: 20 }}>
          <AnswerField
            type="text"
            label="Answer 1"
            placeholder="Enter text"
            name = 'answer1'
            inputRef={ref => this.answer1Ref = ref}
          />
          <AnswerField
            type="text"
            label="Answer 2"
            placeholder="Enter text"
            name = 'answer2'
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
    </div>)
  };
}
