import React from 'react';
import styles from './MovieModal.module.css';

interface RatingSectionProps {
  userRating?: number;
  onRate: (score: number) => void;
  onDelete: () => void;
}

const RatingSection: React.FC<RatingSectionProps> = ({ userRating, onRate, onDelete }) => {
  return (
    <div className={styles.ratingSection}>
      <h4>Evaluation</h4>
      
      <div className={styles.ratingControls}>
        {[1, 2, 3, 4, 5].map((num) => {
          const isActive = userRating === num;
          return (
            <button
              key={num}
              onClick={() => onRate(num)}
              className={`${styles.ratingBtn} ${isActive ? styles.ratingBtnActive : ''}`}
            >
              {num}
            </button>
          );
        })}
      </div>

      {userRating && (
        <button onClick={onDelete} className={styles.deleteBtn}>
          Remove Rating
        </button>
      )}
    </div>
  );
};

export default RatingSection;