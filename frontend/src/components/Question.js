import React from "react";

export const QuestionField = ({ value, label, onChange, name, placeholder }) => (
  <div style={{ display: 'flex', flexDirection: 'row' }}>
    <p style={{ paddingRight: 5 }}>{label}</p>
    <input
      type='text'
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      name={name}
      style={{ width: 300 }}
    />
  </div>
);
