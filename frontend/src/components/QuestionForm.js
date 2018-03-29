/* global process */

import React from "react";
import { Button } from "react-bootstrap";
import { compose, withState } from 'recompose';
import * as R from 'ramda';
import download from 'downloadjs';

import { AnswerField } from "./AnswerField";
import { QuestionField } from "./Question";
import "./AnswerField.css";
import "./QuestionForm.css";

const API_ROOT = process.env.REACT_APP_API_ROOT || 'localhost';
const API_PORT = process.env.REACT_APP_API_PORT || 4545;

const API_ROOT_URL = `http://${API_ROOT}:${API_PORT}`;

const Answers = ({ answers, setAnswers }) => (
  <div className="answers" style={{ marginBottom: 20 }}>
    {answers.map(({ answerText, correct }, index) => (
      <AnswerField
        onChange={e => {
          const clonedAnswers = R.clone(answers);
          clonedAnswers[index].answerText = e.target.value;
          setAnswers(clonedAnswers);
        }}
        key={index}
        value={answers[index].answerText}
        label={`${(10 + index).toString(36)}. `}
        isCorrect={answers[index].correct}
        setIsCorrect={correct => {
          const clonedAnswers = R.clone(answers);
          clonedAnswers[index].correct = correct;
          setAnswers(clonedAnswers);
        }}
      />
    ))}

    <Button
      id = "addAnswerButton"
      bsStyle='info'
      onClick={() => setAnswers(
        [...answers, {answerText: '', correct: false}]
      )}
    >
      Add Answer
    </Button>
  </div>
);

const handleSubmit = state => {
  fetch(`${API_ROOT_URL}/create_project`, {
    method: 'POST',
    body: JSON.stringify(state),
    headers: {
      'Content-Type': 'application/json'
    }}
  )
    .then(res => res.blob())
    .then(blob => download(blob, 'quiz.pdf', 'application/pdf'));
};

const Form = ({ state, setState }) => (
  <div className="form" style={{ width: 520, marginLeft: 20 }}>
    <form>
      <QuestionField
        label="Question: "
        name='question'
        value={state.questionText}
        onChange={e => setState({ ...state, questionText: e.target.value })}
      />

      <div style={{ width: 500, marginLeft: 20, paddingTop: 25 }}>
        <Answers
          answers={state.answers}
          setAnswers={newAnswers => setState({ ...state, answers: newAnswers })}
        />
      </div>

      <Button
        id = "submitButton"
        bsStyle="primary"
        onClick={() => handleSubmit(state)}
      >
        Submit
      </Button>
    </form>
  </div>
);

const initialState = {
  questionText: '',
  answers: [
    {answerText: '', correct: false},
    {answerText: '', correct: false},
    {answerText: '', correct: false}
  ],
};

export default compose(
  withState('state', 'setState', initialState),
)(Form);