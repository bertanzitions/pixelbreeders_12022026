import React, { useState } from 'react';
import CastCard, { CastMember } from './CastCard';
import styles from './MovieModal.module.css';

interface CastSectionProps {
  movieId: number;
}

const API_URL = process.env.REACT_APP_API_URL;

const CastSection: React.FC<CastSectionProps> = ({ movieId }) => {
  const [cast, setCast] = useState<CastMember[]>([]);
  const [showCast, setShowCast] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleToggleCast = async () => {
    // Only fetch if opening and empty
    if (!showCast && cast.length === 0) {
      setIsLoading(true);
      try {
        const res = await fetch(`${API_URL}/cast/${movieId}`);
        if (res.ok) {
          const data = await res.json();
          setCast(data);
        } else {
          console.error("Failed to load cast");
        }
      } catch (error) {
        console.error("Network error loading cast", error);
      } finally {
        setIsLoading(false);
      }
    }
    setShowCast(!showCast);
  };

  return (
    <div className={styles.castSection}>
      <button className={styles.castToggleBtn} onClick={handleToggleCast}>
        {showCast ? 'Hide Cast' : 'Show Cast'}
      </button>

      {showCast && (
        <div className={styles.castContainer}>
          {isLoading ? (
            <p className={styles.castLoading}>Loading cast...</p>
          ) : (
            <div className={styles.castList}>
              {cast.length > 0 ? (
                cast.map((member) => <CastCard key={member.id} member={member} />)
              ) : (
                <p>No cast information available.</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CastSection;