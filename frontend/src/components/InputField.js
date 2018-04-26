import React from 'react';
import "./InputField.css";

/**
 * Simple input field that displays an input component alongside a label.  The input component
 * is passed in as a child.
 */
const InputField = ({ label, children }) => (
  <div style={{ display: 'flex', flexDirection: 'row' }}>
    {label}
    {children}
  </div>
);

export const Input = ({ state, setState, label, stateKey, ...props }) => (
  <InputField label={label}>
    <input
      className='infoInput'
      type='text'
      value={state[stateKey]}
      onChange={e => setState({ ...state, [stateKey]: e.target.value })}
      {...props}
    />
  </InputField>
);

export default InputField;
