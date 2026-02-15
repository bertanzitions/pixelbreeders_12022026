import React from 'react';
import styles from './Input.module.css';

// Extend HTML attributes to allow both Input and Select properties
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement | HTMLSelectElement> {
  options?: { id: number | string; name: string }[];
}

const Input: React.FC<InputProps> = ({ type, className, options, ...props }) => {
  
  // render as select
  if (type === 'select') {
    return (
      <select 
        className={`${styles.input} ${className || ''}`}
        {...(props as React.SelectHTMLAttributes<HTMLSelectElement>)}
      >
        {options ? (
          <>
            {props.placeholder && <option value="">{props.placeholder}</option>}
            
            {options.map((opt) => (
              <option key={opt.id} value={opt.id}>
                {opt.name}
              </option>
            ))}
          </>
        ) : (
          props.children
        )}
      </select>
    );
  }

  // or render normal input
  return (
    <input 
      type={type} // 'text', 'number', 'password', etc.
      className={`${styles.input} ${className || ''}`} 
      {...(props as React.InputHTMLAttributes<HTMLInputElement>)} 
    />
  );
};

export default Input;