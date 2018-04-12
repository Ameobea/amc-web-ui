import React from 'react';
import download from 'downloadjs';
import "./CreateTest.css";

import LoadQuestions from '../components/LoadQuestions';

const handleSubmit = state => {
  fetch(
    './generate_test',
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

const CreateTest = () => (
  <div id='loadingSecton' style={{ diplay: 'flex', flex: 1 }}>
    <h2 id='loadHeader'>Load Existing Questions</h2>
    <LoadQuestions />
  </div>
);

export default CreateTest;
