import React from 'react';
import download from 'downloadjs';

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
  <div style={{ diplay: 'flex', flex: 1 }}>
    <h2>Load Existing Questions</h2>
    <LoadQuestions />
  </div>
);

export default CreateTest;
