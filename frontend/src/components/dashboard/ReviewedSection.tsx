import React from 'react';
import { RatedMovie } from '../../types';
import MovieCard from '../search/MovieCard';

interface ReviewedSectionProps {
  movies: RatedMovie[];
  onMovieClick: (movie: RatedMovie) => void;
}

const ReviewedSection: React.FC<ReviewedSectionProps> = ({ movies, onMovieClick }) => {
  return (
    <div className="page-reviewed">
      {movies.length === 0 && <p>No reviewed movies yet.</p>}
      <div className="movie-grid">
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