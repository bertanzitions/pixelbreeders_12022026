import React, { forwardRef } from 'react';
import { Movie, RatedMovie } from '../../../types';
import FilmIcon from '../../misc/FilmIcon';
import styles from './MovieCard.module.css';

interface MovieCardProps {
  movie: Movie | RatedMovie;
  onClick: (movie: Movie | RatedMovie) => void;
}

const MovieCard = forwardRef<HTMLDivElement, MovieCardProps>(({ movie, onClick }, ref) => {
  const rating = (movie as RatedMovie).userRating;

  return (
    <div ref={ref} className={styles.card} onClick={() => onClick(movie)}>
      {movie.poster_path ? (
        <img src={movie.poster_path} alt={movie.title} />
      ) : (
        <div className={styles.noImage}>
          <FilmIcon />
          <span>Image Unavailable</span>
        </div>
      )}
      
      <div className={styles.content}>
        <h3>{movie.title}</h3>
        {rating && <p>Rating: <strong>{rating}/5</strong></p>}
      </div>
    </div>
  );
});

export default MovieCard;