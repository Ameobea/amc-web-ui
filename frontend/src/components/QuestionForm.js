import React from "react";
import { Button } from "react-bootstrap";
import { compose, withState } from 'recompose';
import * as R from 'ramda';

import { AnswerField } from "./AnswerField";
import { QuestionField } from "./Question";
import InputField from './InputField';
import "./AnswerField.css";
import "./QuestionForm.css";

const getEmptyQuestion = () => ({
  questionText: '',
  answers: [
    {answerText: '', correct: false},
    {answerText: '', correct: false},
    {answerText: '', correct: false}
  ],
  // Does question contain text?
  questionValid: false
});

const Answers = ({ answers, setAnswers, removeAnswer }) => (
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
    <Button
      id = "addAnswerButton"
      bsStyle='info'
      onClick={() => {
        const newAnswers= R.remove(answers.length-1, 1, answers);
        setAnswers(newAnswers);
      }}
    >
      Remove Question
    </Button>
  </div>
);

// Tests if given input has text
const answerHasText = (answer) => {
  return answer.answerText !== '';
};

const handleSubmit = state => {
  // An array of boolean values stating whether or not each answer has text
  const answersValid = state.questions.reduce(
    (acc, { questionValid, answers }) => acc && questionValid && !answers.find(answer => !answerHasText(answer)),
    true
  );

  if(!answersValid) {
    return alert("All fields are required");
  }

  fetch(
    './store_questions',
    {
      method: 'POST',
      body: JSON.stringify(state),
      headers: {
        'Content-Type': 'application/json'
      },
    }
  )
    .then(res => res.text())
    .then(res => alert(res));
};

const Question = ({ state, setState }) => (
  <div style={{ paddingBottom: 25 }}>
    <QuestionField
      label="Question: "
      name='question'
      id='question'
      value={state.questionText}
      // Changes question state and questionValid state
      onChange={e => setState({ ...state, questionText: e.target.value, questionValid: true })}
    />

    <div style={{ width: 500, marginLeft: 20, paddingTop: 25 }}>
      <Answers
        answers={state.answers}
        setAnswers={newAnswers => setState({ ...state, answers: newAnswers })}
      />
    </div>
  </div>
);

const FormControls = ({ state, setState }) => (
  <div>
    <div style={{ paddingBottom: 25 }}>
      <InputField label='Username (optional):'>
        <input class='infoInput' id='username'
          type='text'
          value={state.username || ''}
          onChange={e => setState({ ...state, username: e.target.value })}
        />
      </InputField>

      <InputField label='Topic / Tag:'>
        <input class='infoInput' id='topic'
          type='text'
          value={state.topic || ''}
          onChange={e => setState({ ...state, topic: e.target.value })}
        />
      </InputField>

      <InputField label='Share question publically?:'>
        <input class='infoInput'
          id="checkBox"
          type="checkbox"
          style={{ width: 20, marginRight: 5 }}
          checked={state.shared}
          onChange={() => setState({ ...state, shared: !state.shared })}
        />
      </InputField>
    </div>

    <div style={{ flexDirection: "row" }}>
      <Button
        id="submitButton"
        bsStyle="primary"
        onClick={() => setState({...state, questions: R.append(getEmptyQuestion(), state.questions) })}
        style={{ marginTop: 0, marginRight: 10 }}
      >
        Add Question
      </Button>

      <Button
        id="submitButton"
        bsStyle="primary"
        onClick={() => handleSubmit(state)}
      >
        Submit
      </Button>
    </div>
  </div>
);

const Form = ({ state, setState }) => (
  <div className="form" style={{ width: 520, marginLeft: 20 }}>
    <form>
      <div>
        {state.questions.map((questionState, i) => (
          <Question
            key={i}
            state={questionState}
            setState={newState => setState({...state, questions: R.update(i, newState, state.questions) })}
          />
        ))}
      </div>

      <hr />

      <FormControls state={state} setState={setState} />
    </form>
  </div>
);

const initialState = {
  username: null,
  shared: true,
  questions: [getEmptyQuestion()],
};

export default compose(
  withState('state', 'setState', initialState),
)(Form);
