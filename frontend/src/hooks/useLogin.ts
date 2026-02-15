import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const API_URL = process.env.REACT_APP_API_URL;

export const useLogin = () => {
  const { login } = useAuth();
  
  const [isRegistering, setIsRegistering] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const toggleMode = () => {
    setIsRegistering((prev) => !prev);
    setError(''); // Clear errors when switching modes
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const endpoint = isRegistering ? '/auth/register' : '/auth/login';

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.msg || 'An error occurred');
      }

      if (isRegistering) {
        setIsRegistering(false);
        setError('Registration successful! Please log in.');
      } else {
        login(data.access_token, email);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  return {
    // state
    isRegistering,
    email,
    setEmail,
    password,
    setPassword,
    error,
    
    // handlers
    handleSubmit,
    toggleMode
  };
};