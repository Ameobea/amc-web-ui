import React from 'react';
import './Grade.css';
import Dropzone from 'react-dropzone';

const handleDrop = files => {
  if(files.length === 0) { return; }

  const payload = new FormData();
  payload.append('file', files[0]);

  fetch('./grade_test', { method: 'POST', body: payload })
    .then(res => res.json())
    .then(res => console.log(res));
};

const Grade = () => (
  <div>
    <Dropzone id = 'dropzone' onDrop={handleDrop}>
      <p>Drag scanned tests to be graded and drop them here.</p>
    </Dropzone>
    <div id="bottomspace">
    </div>
  </div>
);

export default Grade;
