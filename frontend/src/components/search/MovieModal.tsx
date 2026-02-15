import React from 'react';
import { RatedMovie } from '../../types';
import styles from './MovieModal.module.css';

interface MovieModalProps {
  movie: RatedMovie;
  onClose: () => void;
  onRate: (score: number) => void;
  onDelete: () => void;
}

const MovieModal: React.FC<MovieModalProps> = ({ movie, onClose, onRate, onDelete }) => {
  return (
    <div className={styles.overlay} onClick={onClose}>
      {/* avoid clicking inside the modal close it */}
      <div className={styles.content} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeButton} onClick={onClose}>×</button>

        <h2 className={styles.title}>{movie.title}</h2>

        {movie.backdrop_path && (
          <img
            src={`https://image.tmdb.org/t/p/w500${movie.backdrop_path}`}
            alt="Backdrop"
            className={styles.backdrop}
          />
        )}

        <p><strong>Release Date:</strong> {movie.release_date || 'Unknown'}</p>
        <p>{movie.overview || 'No synopsis available.'}</p>

        <div className={styles.ratingSection}>
          <h4>Evaluation</h4>
          
          <div className={styles.ratingControls}>
            {[1, 2, 3, 4, 5].map((num) => {
              // Determine if this button represents the current user rating
              const isActive = movie.userRating === num;
              
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

          {movie.userRating && (
            <button onClick={onDelete} className={styles.deleteBtn}>
              Remove Rating
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default MovieModal;