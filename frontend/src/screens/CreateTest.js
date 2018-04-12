import React from 'react';
import download from 'downloadjs';
import { withState } from 'recompose';
import { Table } from 'react-bootstrap';

import LoadQuestions from '../components/LoadQuestions';
import "./CreateTest.css";

const getInitialState = () => ({
  questions: [],
});

const handleSubmit = questions => {
  fetch(
    './create_project',
    {
      method: 'POST',
      body: JSON.stringify(questions),
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

const Answers = ({ answers }) => (
  <Table condensed>
    <tbody>
      {answers.map(({ answerText }, i) => (
        <tr key={i}>
          <td>`{i}. {answerText}`</td>
        </tr>
      ))}
    </tbody>
  </Table>
);

const TestPreview = ({ questions }) => (
  <div>
    <h2>Create Test</h2>

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

    <button onClick={() => handleSubmit(questions)}>Generate</button>
  </div>
);

const CreateTest = ({ state, setState }) => (
  <div id='loadingSecton' style={{ diplay: 'flex', flex: 1 }}>
    <h2 id='loadHeader'>Load Existing Questions</h2>
    <LoadQuestions onQuestionsSelected={questions => setState({ ...state, questions })} />

    <TestPreview questions={state.questions} />
  </div>
);

export default withState('state', 'setState', getInitialState())(CreateTest);
