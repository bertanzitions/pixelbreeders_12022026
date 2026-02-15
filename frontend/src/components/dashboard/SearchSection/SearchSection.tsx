import React from 'react';
import { Movie } from '../../../types';
import Input from '../../misc/Input';
import Button from '../../misc/Button';
import MovieCard from '../../search/MovieCard';
import styles from './SearchSection.module.css';

interface SearchSectionProps {
  query: string;
  setQuery: (q: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  results: Movie[];
  lastElementRef: (node: HTMLDivElement | null) => void;
  onMovieClick: (movie: Movie) => void;
  isLoading: boolean;
}

const SearchSection: React.FC<SearchSectionProps> = ({
  query,
  setQuery,
  onSubmit,
  results,
  lastElementRef,
  onMovieClick,
  isLoading
}) => {
  return (
    <div className={styles.container}>
      <form className={styles.searchBarForm} onSubmit={onSubmit}>
        <Input 
          type="text" 
          placeholder="Search..." 
          value={query} 
          onChange={e => setQuery(e.target.value)}
          style={{ flex: 1 }} 
        />
        <Button type="submit">Search</Button>
      </form>
      
      <div className={styles.movieGrid}>
        {results.map((movie, index) => {
          const isLast = results.length === index + 1;
          return (
            <MovieCard 
              key={`${movie.tmdb_id}-${index}`}
              ref={isLast ? lastElementRef : null}
              movie={movie} 
              onClick={onMovieClick} 
            />
          );
        })}
      </div>
      
      {isLoading && <p className={styles.loading}>Loading...</p>}
    </div>
  );
};

export default SearchSection;