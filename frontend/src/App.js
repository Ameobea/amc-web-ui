import React, { Component } from "react";
import {
  Button,
  FormControl,
  ControlLabel,
  FormGroup,
  HelpBlock,
} from "react-bootstrap";
import "./App.css";
import Form from "./form.js";


class App extends React.Component {
  handleSubmit = () => {
    alert(this.questionNameRef.value + this.answer1Ref.value + this.answer2Ref.value + this.answer3Ref.value + this.answer4Ref.value);
  }

  render = () => (
    <div>
      <h1 style={{fontSize: 28, fontFamily:'times'}}>Enter your question, answers, and check correct answers.</h1>
      <Form />
    </div>
  );
}

export default App;
