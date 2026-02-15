import React from 'react';

const ErrorMessage = ({ message }: { message: string }) => {
  if (!message) return null;
  return <p style={{ color: 'red', margin: '10px 0' }}>{message}</p>;
};

export default ErrorMessage;