import React, { useState } from 'react';
// Import the necessary components and styles from react-mathquill
import { addStyles, EditableMathField } from 'react-mathquill';

// Add MathQuill styles
addStyles();

const MathInput = () => {
  const [latex, setLatex] = useState('');

  const handleLatexChange = (mathField) => {
    // Update the state with the new LaTeX value
    setLatex(mathField.latex());
    console.log(mathField.latex());
  };

  return (
    <div>
      <p>Type your math here:</p>
      <EditableMathField
        latex={latex} // The LaTeX value
        onChange={handleLatexChange} // Handler for changes
        style={{ border: '1px solid #ccc', padding: '5px' }}
      />
      <p>LaTeX output:</p>
      <div style={{ border: '1px solid #ccc', padding: '5px' }}>
        {latex}
      </div>
    </div>
  );
};

export default MathInput;
