import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'link';
}

const Button: React.FC<ButtonProps> = ({ variant = 'primary', style, children, ...props }) => {
  // style for link variant
  const linkStyle: React.CSSProperties = {
    background: 'none', 
    border: 'none', 
    textDecoration: 'underline', 
    cursor: 'pointer', 
    color: 'blue',
    padding: 0
  };

  // styles for normal button
  const primaryStyle: React.CSSProperties = {
    padding: '8px 15px',
    cursor: 'pointer',
    background: '#efefef',
    border: '1px solid black'
  };

  return (
    <button 
      style={{ ...(variant === 'link' ? linkStyle : primaryStyle), ...style }} 
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;