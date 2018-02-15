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

export const AnswerField = ({ value, label, onChange, name, placeholder }) => (
  <div>
    <p>{label}</p>
    <input id="checkBox" type="checkbox" style={{width: 20}}/>
    <input type='text' value={value} onChange={onChange} placeholder={placeholder} name={name} />
  </div>
)
