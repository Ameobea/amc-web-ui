import React from 'react';
import download from 'downloadjs';
import { withState } from 'recompose';
import { Table } from 'react-bootstrap';

import LoadQuestions from '../components/LoadQuestions';
import InputField from '../components/InputField';
import "./CreateTest.css";

const handleSubmit = state => {
  fetch(
    './create_project',
    {
      method: 'POST',
      body: JSON.stringify(state),
      headers: {
        'Content-Type': 'application/json'
      },
    }
  )
    .then(res => res.blob())
    .then(blob => download(blob, 'quiz.pdf', 'application/pdf'));
};

const TestPreviewHeader = () => (
  <thead>
    <tr>
      <th>#</th>
      <th>Topic</th>
      <th>Username</th>
      <th>Question</th>
      <th>Answers</th>
    </tr>
  </thead>
);

const Answers = ({ answers = [] }) => (
  <Table condensed>
    <tbody>
      {answers.map(({ answerText }, i) => (
        <tr key={i}>
          <td>{`${i}. ${answerText}`}</td>
        </tr>
      ))}
    </tbody>
  </Table>
);

const getInitialTestPreviewState = () => ({
  name: 'Test Name',
  username: 'Your Username',
});

const TestPreview = withState('state', 'setState', getInitialTestPreviewState())(
  ({ questions, state, setState }) => (
    <div>
      <h2 id='createHeader'>Create Test</h2>

      <Table striped bordered condensed responsive>
        <TestPreviewHeader />

        <tbody>
          {questions.map(({ topic, username, questionText, answers }, i) => (
            <tr key={i}>
              <td>{i}</td>
              <td>{topic}</td>
              <td>{username}</td>
              <td>{questionText}</td>
              <td><Answers answers={answers} /></td>
            </tr>
          ))}
        </tbody>
      </Table>

      <div class='createForm'>
        <InputField label='Test Name: '>
          <input
            class='infoInput'
            id='test'
            type='text'
            value={state.name}
            onChange={e => setState({ ...state, name: e.target.value })}
          />
        </InputField>
        <InputField label='Username: '>
          <input
            class='infoInput'
            id='name'
            type='text'
            value={state.username}
            onChange={e => setState({ ...state, username: e.target.value })}
          />
        </InputField>

        <button
          id='generateButton'
          type='button'
          onClick={() => handleSubmit({ ...state, questions })}
        >
          Generate
        </button>
      </div>
    </div>
  )
);

const CreateTest = ({ questions, setQuestions }) => (
  <div id='loadingSecton' style={{ diplay: 'flex', flex: 1 }}>
    <h2 id='loadHeader'>Load Existing Questions</h2>
    <LoadQuestions onQuestionsSelected={setQuestions} />

    <TestPreview questions={questions} />
  </div>
);

export default withState('questions', 'setQuestions', [])(CreateTest);
