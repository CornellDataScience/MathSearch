import React from 'react';

function MathKeyboard({ onSymbolSelect, isVisible }) {
  if (!isVisible) return null;

  const symbols = [
    { label: '∑', latex: '\\sum_{lower}^{upper}' },
    { label: '∫', latex: '\\int{}' },
    { label: '∏', latex: '\\prod{}' },
    { label: '√', latex: '\\sqrt{}' },
    { label: 'n√', latex: '\\sqrt[n]{}' },
    { label: 'x²', latex: '{x}^{2}' },
    { label: 'x²', latex: '{x}^{2}' },
    { label: 'xʸ', latex: '{x}^{y}' },
    { label: 'ₓ√y', latex: '\\sqrt[x]{y}' },
    { label: 'log', latex: '\\log{}' },
    { label: 'ln', latex: '\\ln{}' },
    { label: 'eˣ', latex: 'e^{x}' },
    { label: '10ˣ', latex: '10^{x}' },
    { label: '∂', latex: '\\partial{}' },
    { label: '∂²', latex: '\\partial^{2}{}' },
    { label: '∂/∂x', latex: '\\frac{\\partial}{\\partial x}{}' },
    { label: '∂²/∂x²', latex: '\\frac{\\partial^{2}}{\\partial x^{2}}{}' },
    { label: '∬', latex: '\\iint{}' },
    { label: '∭', latex: '\\iiint{}' },
    { label: 'lim', latex: '\\lim_{}' },
    { label: '[a,b]', latex: '[a,b]' },
    { label: '(', latex: '\\left(' },
    { label: ')', latex: '\\right)' },
    { label: '{', latex: '\\left\\{' },
    { label: '}', latex: '\\right\\}' }
  ];


  return (
    <div className="math-keyboard">
      {symbols.map((symbol, index) => (
        <button
          key={index}
          className="math-symbol-btn"
          onMouseDown={(e) => e.preventDefault()} // Prevent the default mouse down behavior
          onClick={() => onSymbolSelect(symbol.latex)}
        >
          {symbol.label}
        </button>

      ))}
    </div>
  );
}

export default MathKeyboard;
