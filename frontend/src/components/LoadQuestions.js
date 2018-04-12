/**
 * Form for loading questions from the database for use in tests.
 */
import "./LoadQuestions.css";
import React from 'react';
import { withState } from 'recompose';
import { Table } from 'react-bootstrap';

import InputField from './InputField';

const getInitialState = () => ({
  topic: null,
  username: null,
  questionText: null,
  dbResponse: null,
});

/**
 * Make a query to the backend to fetch all questions from the database that match the
 * provided query.
 */
const handleSubmit = (state, setState) => {
  const { topic, username, questionText } = state;
  const query = { topic, username, question_text: questionText };

  fetch(
    './find_questions',
    {
      method: 'POST',
      body: JSON.stringify(query),
      headers: {
        'Content-Type': 'application/json'
      },
    }
  )
    .then(res => res.json())
    .then(dbResponse => setState({ ...state, dbResponse }));
};

const LoadedQuestionsHeader = () => (
  <thead>
    <tr>
      <th>Topic</th>
      <th>Username</th>
      <th>Question</th>
    </tr>
  </thead>
);

const LoadedQuestions = ({ dbResponse }) => {
  if(dbResponse === null) {
    return null;
  }

  return (
    <div style={{ display: 'flex', flex: 1, paddingTop: 25 }}>
      <Table striped bordered condensed responsive>
        <LoadedQuestionsHeader />

        <tbody>
          {dbResponse.map(({ topic, username, questionText }, i) => (
            <tr key={i}>
              <td>{topic}</td>
              <td>{username}</td>
              <td>{questionText}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

const LoadQuestions = ({ state, setState }) => (
  <div class='loadForm' style={{ diplay: 'flex', flex: 1 }}>
    <InputField label='Topic (optional): '>
      <input class='infoInput' id='topic'
        type='text'
        value={state.topic || ''}
        onChange={e => setState({ ...state, topic: e.target.value })}
      />
    </InputField>
    <InputField label='Username (optional): '>
      <input class='infoInput' id='username'
        type='text'
        value={state.username || ''}
        onChange={e => setState({ ...state, username: e.target.value })}
      />
    </InputField>
    <InputField label='Question Contains Text (optional): '>
      <input class='infoInput' id='contains'
        type='text'
        value={state.questionText || ''}
        onChange={e => setState({ ...state, questionText: e.target.value })}
      />
    </InputField>

    <button id='loadButton' onClick={() => handleSubmit(state, setState)} >Submit Query</button>

    <LoadedQuestions dbResponse={state.dbResponse} />
  </div>
);

export default withState('state', 'setState', getInitialState())(LoadQuestions);
