import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input: React.FC<InputProps> = (props) => {
  return (
    <input 
      style={{ padding: '8px', border: '1px solid black' }} 
      {...props} 
    />
  );
};

export default Input;