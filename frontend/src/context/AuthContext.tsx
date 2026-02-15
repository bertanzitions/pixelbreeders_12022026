import React, { createContext, useState, useEffect, useContext } from 'react';
import { User } from '../types';

interface AuthContextType {
  user: User | null;
  login: (token: string, email: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>(null!);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('email');
    if (token && email) {
      setUser({ token, email });
    }
  }, []);

  const login = (token: string, email: string) => {
    localStorage.setItem('token', token);
    localStorage.setItem('email', email);
    setUser({ token, email });
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);