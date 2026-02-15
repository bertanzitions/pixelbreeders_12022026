import React from 'react';
import { useAuth } from '../../context/AuthContext';

interface NavbarProps {
  currentView: 'search' | 'reviewed';
  setView: (view: 'search' | 'reviewed') => void;
}

const Navbar: React.FC<NavbarProps> = ({ currentView, setView }) => {
  const { user, logout } = useAuth();

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid black', marginBottom: '20px' }}>
      <nav style={{ border: 'none', marginBottom: 0 }}>
        <button className={currentView === 'search' ? 'active' : ''} onClick={() => setView('search')}>
          Search
        </button>
        <button className={currentView === 'reviewed' ? 'active' : ''} onClick={() => setView('reviewed')}>
          Reviewed
        </button>
      </nav>
      <div>
        <span style={{ marginRight: '10px' }}>{user?.email}</span>
        <button onClick={logout}>Logout</button>
      </div>
    </div>
  );
};

export default Navbar;