import React, { Component } from "react";
import {
  Button,
  FormControl,
  ControlLabel,
  FormGroup,
  HelpBlock,
} from "react-bootstrap";
import "./App.css";

export const QuestionField = ({ value, label, onChange, name, placeholder }) => (
  <div>
    <p>{label}</p>
    <input type='text' value={value} onChange={onChange} placeholder={placeholder} name={name} />
  </div>
)
