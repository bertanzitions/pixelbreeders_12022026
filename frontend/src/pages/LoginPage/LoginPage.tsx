import React from 'react';
import { useLogin } from '../../hooks/useLogin';
import Input from '../../components/misc/Input';
import Button from '../../components/misc/Button';
import ErrorMessage from '../../components/misc/ErrorMessage';

const LoginPage = () => {
  const {
    isRegistering,
    email,
    setEmail,
    password,
    setPassword,
    error,
    handleSubmit,
    toggleMode
  } = useLogin();

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', border: '1px solid black', padding: '20px' }}>
      <h2>{isRegistering ? 'Register' : 'Login'}</h2>
      
      <ErrorMessage message={error} />
      
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <Input 
          type="email" 
          placeholder="Email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          required 
        />
        <Input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          required 
        />
        <Button type="submit">
          {isRegistering ? 'Register' : 'Login'}
        </Button>
      </form>
      
      <p style={{ marginTop: '10px', fontSize: '0.9em' }}>
        {isRegistering ? "Already have an account? " : "Don't have an account? "}
        <Button variant="link" onClick={toggleMode} type="button">
          {isRegistering ? 'Login here' : 'Register here'}
        </Button>
      </p>
    </div>
  );
};

export default LoginPage;