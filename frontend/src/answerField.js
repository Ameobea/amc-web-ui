import React, { Component } from "react";
import {
  Button,
  FormControl,
  ControlLabel,
  FormGroup,
  HelpBlock,
} from "react-bootstrap";
import "./App.css";
import "./answerField.css";

const FieldGroup = ({ id, label, help, ...props }) => (
  <FormGroup controlId={id}>
    <ControlLabel>{label}</ControlLabel>
    <FormControl {...props} />
    {help && <HelpBlock>{help}</HelpBlock>}
  </FormGroup>
);

export class AnswerField extends React.Component
{
  constructor(props)
  {
    super(props);
  }

  render()
  {
    return(
    <div className="answerContainer">
      <input id="checkBox" type="checkbox" style={{width: 20}}/>
      <FieldGroup
        type={this.props.text}
        label={this.props.label}
        placeholder={this.props.placeholder}
        ref = {this.inputRef}
        style = {{width: 490}}
      />
    </div>)
  }
}
