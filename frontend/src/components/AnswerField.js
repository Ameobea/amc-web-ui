import React from "react";

import "./AnswerField.css";

export const AnswerField = ({
  value,
  label,
  onChange,
  name,
  placeholder,
  isCorrect,
  setIsCorrect
}) => (
  <div style={{ display: 'flex', flexDirection: 'row', paddingBottom: 10 }}>
    <span style={{ paddingRight: 4 }}>{label}</span>

    <input
      id="checkBox"
      type="checkbox"
      style={{ width: 20, marginRight: 5 }}
      checked={isCorrect}
      onChange={() => setIsCorrect(!isCorrect)}
    />

    <input
      type='text'
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      name={name}
    />
  </div>
);
