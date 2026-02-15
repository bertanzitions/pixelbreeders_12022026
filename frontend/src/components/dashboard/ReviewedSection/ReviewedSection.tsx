import React from 'react';
import { RatedMovie } from '../../../types';
import MovieCard from '../../search/MovieCard';
import styles from './ReviewedSection.module.css';

interface ReviewedSectionProps {
  movies: RatedMovie[];
  onMovieClick: (movie: RatedMovie) => void;
}

const ReviewedSection: React.FC<ReviewedSectionProps> = ({ movies, onMovieClick }) => {
  return (
    <div className={styles.container}>
      {movies.length === 0 && (
        <p className={styles.emptyMessage}>No reviewed movies yet.</p>
      )}
      
      <div className={styles.movieGrid}>
        {movies.map(movie => (
          <MovieCard 
            key={movie.tmdb_id} 
            movie={movie} 
            onClick={onMovieClick} 
          />
        ))}
      </div>
    </div>
  );
};

export default ReviewedSection;