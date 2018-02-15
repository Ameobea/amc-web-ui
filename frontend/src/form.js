import React, { Component } from "react";
import {
  Button,
  FormControl,
  ControlLabel,
  FormGroup,
  HelpBlock,
} from "react-bootstrap";
import { compose, withState } from 'recompose';

import "./App.css";
import { AnswerField } from "./answerField.js";
import "./answerField.css";

const PopulatedAnswerField = ({ values, setValues, name, ...props }) => (
  <AnswerField
    onChange={e => setValues({ ...values, [name]: e.target.value })}
    value={values[name]}
    name={name}
    {...props}
  />
)

const Answers = ({ answerNames, setanswerNames, values, setValues }) => (
  <div>
    {answerNames.map(({ name, label}) => (
      <PopulatedAnswerField
        values={values}
        setValues={setValues}
        name={name}
        label={label}
      />
    ))}

    <Button onClick={() => setanswerNames([
      ...answerNames,
      {
        name: `answer${answerNames.length + 1}`,
        label: `Answer ${answerNames.length + 1}`,
      }
    ])}>
      Add Question
    </Button>
  </div>
)

const handleSubmit = values => {
  alert(JSON.stringify(values))
}

const Form = ({ values, setValues, answerNames, setanswerNames }) => (
  <div style={{ width: 520, marginLeft: 20 }}>
    <form>
      <div style={{ width: 500, marginLeft: 20 }}>
        <Answers
          answerNames={answerNames}
          setanswerNames={setanswerNames}
          values={values}
          setValues={setValues}
        />
      </div>

      <Button
        bsStyle="primary"
        onClick={() => handleSubmit(values)}
      >
        Submit
      </Button>
    </form>
  </div>
)

export default compose(
  withState('values', 'setValues', {}),
  withState('answerNames', 'setanswerNames', [
    {label: 'Answer 1', name: 'answer1'},
    {label: 'Answer 2', name: 'answer2'},
    {label: 'Answer 3', name: 'answer3'},
  ]),
)(Form);
