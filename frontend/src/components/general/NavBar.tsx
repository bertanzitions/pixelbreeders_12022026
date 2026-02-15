import React from 'react';
import { useAuth } from '../../context/AuthContext';
import styles from './NavBar.module.css';
import logo from '../../assets/logo.png';

interface NavbarProps {
  currentView: 'search' | 'reviewed';
  setView: (view: 'search' | 'reviewed') => void;
}

const Navbar: React.FC<NavbarProps> = ({ currentView, setView }) => {
  const { user, logout } = useAuth();

  return (
    <header className={styles.navbar}>
      <div className={styles.leftSection}>
        <img 
          src={logo} 
          alt="Blockbuster Logo" 
          className={styles.logo} 
          onClick={() => setView('search')}
        />

        <nav className={styles.navLinks}>
          <button 
            className={`${styles.navButton} ${currentView === 'search' ? styles.active : ''}`} 
            onClick={() => setView('search')}
          >
            Search
          </button>
          <button 
            className={`${styles.navButton} ${currentView === 'reviewed' ? styles.active : ''}`} 
            onClick={() => setView('reviewed')}
          >
            My Reviews
          </button>
        </nav>
      </div>

      <div className={styles.userSection}>
        <span className={styles.email}>{user?.email}</span>
        <button onClick={logout} className={styles.logoutBtn}>
          Logout
        </button>
      </div>
    </header>
  );
};

export default Navbar;