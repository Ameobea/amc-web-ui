import React from "react";
import { Button } from "react-bootstrap";
import { compose, withState } from 'recompose';
import * as R from 'ramda';

import { AnswerField } from "./AnswerField";
import { QuestionField } from "./Question";
import "./AnswerField.css";

const Answers = ({ answers, setAnswers }) => (
  <div>
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
  </div>
);

const handleSubmit = state => {
  alert(JSON.stringify(state, null, 2));
};

const Form = ({ state, setState }) => (
  <div style={{ width: 520, marginLeft: 20 }}>
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
