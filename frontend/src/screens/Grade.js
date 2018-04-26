import React from 'react';
import './Grade.css';
import download from 'downloadjs';
import Dropzone from 'react-dropzone';
import { withState } from 'recompose';

import { Input } from '../components/InputField';

const handleDrop = (state, files) => {
  if(files.length === 0) { return; }

  const payload = new FormData();
  payload.append('file', files[0]);
  Object.keys(state).forEach(key => payload.append(key, state[key]));

  fetch('./grade_test', { method: 'POST', body: payload })
    .then(res => {
      if(res.status !== 200) {
        return res.json().then(({ message }) => { throw message; });
      }

      return res.blob();
    })
    .then(blob => download(blob, 'zooms_and_crops.zip', 'application/zip'));
};

const Grade = withState('state', 'setState', {})(
  ({ state, setState }) => (
    <div>
      <Input state={state} setState={setState} label='Test name: ' stateKey='testName' />
      <Input state={state} setState={setState} label='Username: ' stateKey='username' />
      <br />

      <Dropzone id = 'dropzone' onDrop={files => handleDrop(state, files)}>
        <p>Drag scanned tests to be graded and drop them here.</p>
      </Dropzone>
    </div>
  )
);

export default () => <div style={{ padding: 30 }}><Grade /></div>;
