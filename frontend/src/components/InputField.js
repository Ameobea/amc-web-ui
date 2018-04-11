import React from 'react';

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

export default InputField;
