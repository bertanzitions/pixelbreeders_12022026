import React from 'react';
import { Movie } from '../../types';
import Input from '../misc/Input';
import Button from '../misc/Button';
import MovieCard from '../search/MovieCard';

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
    <div className="page-search">
      <form 
        className="search-bar" 
        onSubmit={onSubmit} 
        style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}
      >
        <Input 
          type="text" 
          placeholder="Search..." 
          value={query} 
          onChange={e => setQuery(e.target.value)}
          style={{ flex: 1, padding: '8px' }} 
        />
        <Button type="submit">Search</Button>
      </form>
      
      <div className="movie-grid">
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
      
      {isLoading && <p style={{textAlign: 'center', padding: '20px'}}>Loading...</p>}
    </div>
  );
};

export default SearchSection;