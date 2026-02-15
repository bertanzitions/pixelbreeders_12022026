import React from 'react';
import { useLogin } from '../../hooks/useLogin';
import Input from '../../components/misc/Input';
import Button from '../../components/misc/Button';
import ErrorMessage from '../../components/misc/ErrorMessage';
import styles from './LoginPage.module.css';

const LoginPage = () => {
  const {
    isRegistering,
    email, setEmail,
    password, setPassword,
    confirmPassword, setConfirmPassword,
    error,
    handleSubmit,
    toggleMode
  } = useLogin();

  return (
    <div className={styles.pageWrapper}>
      <div className={styles.loginCard}>
        <h2>{isRegistering ? 'Join the Club' : 'Welcome Back'}</h2>
        
        <ErrorMessage message={error} />
        
        <form onSubmit={handleSubmit} className={styles.form}>
          <Input 
            type="email" 
            placeholder="Email Address" 
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

          {isRegistering && (
            <Input 
              type="password" 
              placeholder="Confirm Password" 
              value={confirmPassword} 
              onChange={(e) => setConfirmPassword(e.target.value)} 
              required 
            />
          )}

          <Button type="submit">
            {isRegistering ? 'Register' : 'Login'}
          </Button>
        </form>
        
        <p className={styles.toggleText}>
          {isRegistering ? "Already a member? " : "Not a member yet? "}
          <Button variant="link" onClick={toggleMode} type="button">
            {isRegistering ? 'Login here' : 'Register here'}
          </Button>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;