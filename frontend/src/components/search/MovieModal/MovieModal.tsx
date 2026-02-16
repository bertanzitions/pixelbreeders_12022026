import React from 'react';
import { RatedMovie } from '../../../types';
import styles from './MovieModal.module.css';
import CastSection from './CastSection';
import RatingSection from './RatingSection';

interface MovieModalProps {
  movie: RatedMovie;
  onClose: () => void;
  onRate: (score: number) => void;
  onDelete: () => void;
}

const MovieModal: React.FC<MovieModalProps> = ({ movie, onClose, onRate, onDelete }) => {
  return (
    <div className={styles.overlay} onClick={onClose}>
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

        <CastSection movieId={movie.tmdb_id} />
        
        <RatingSection 
          userRating={movie.userRating} 
          onRate={onRate} 
          onDelete={onDelete} 
        />
      </div>
    </div>
  );
};

export default MovieModal;