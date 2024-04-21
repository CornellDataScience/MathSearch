import React from 'react';

function MathKeyboard({ onSymbolSelect, isVisible }) {
  if (!isVisible) return null;

  const symbols = [
    { label: '∑', latex: '\\sum{}' },
    { label: '√', latex: '\\sqrt{}' },
    // ... other symbols as needed
  ];

  return (
    <div className="math-keyboard">
      {symbols.map((symbol, index) => (
        <button
          key={index}
          className="math-symbol-btn"
          onClick={() => onSymbolSelect(symbol.latex)}
        >
          {symbol.label}
        </button>
      ))}
    </div>
  );
}

export default MathKeyboard;
