import React from 'react';
import { Movie, Genre } from '../../../types';
import Input from '../../misc/Input';
import Button from '../../misc/Button';
import MovieCard from '../../search/MovieCard';
import styles from './SearchSection.module.css';

interface SearchSectionProps {
  query: string;
  setQuery: (q: string) => void;
  year: string;
  setYear: (y: string) => void;
  genre: string;
  setGenre: (g: string) => void;
  genresList: Genre[];
  onSubmit: (e: React.FormEvent) => void;
  results: Movie[];
  lastElementRef: (node: HTMLDivElement | null) => void;
  onMovieClick: (movie: Movie) => void;
  isLoading: boolean;
}

const SearchSection: React.FC<SearchSectionProps> = ({
  query, setQuery,
  year, setYear,
  genre, setGenre,
  genresList,
  onSubmit,
  results,
  lastElementRef,
  onMovieClick,
  isLoading
}) => {
  return (
    <div className={styles.container}>
      <form className={styles.searchBarForm} onSubmit={onSubmit}>
        <div className={styles.filtersRow}>
          
          {/* Title*/}
          <div className={styles.inputGroup} style={{ flex: 2, minWidth: '200px' }}>
            <label className={styles.label}>Title</label>
            <Input 
              type="text" 
              placeholder="Search by title..." 
              value={query} 
              onChange={e => setQuery(e.target.value)}
              style={{ width: '100%' }} 
            />
          </div>
          
          {/* Year */}
          <div className={styles.inputGroup} style={{ flex: 1, minWidth: '100px' }}>
            <label className={styles.label}>Year</label>
            <Input 
              type="number" 
              placeholder="Ex: 2023" 
              value={year}
              min={1800}
              onChange={e => setYear(e.target.value)}
              style={{ width: '100%' }} 
            />
          </div>

          {/* Genre */}
          <div className={styles.inputGroup} style={{ flex: 1, minWidth: '150px' }}>
            <label className={styles.label}>Genre</label>
            <select 
              className={styles.selectInput}
              value={genre} 
              onChange={e => setGenre(e.target.value)}
            >
              <option value="">All Genres</option>
              {genresList.map((g) => (
                <option key={g.id} value={g.id}>
                  {g.name}
                </option>
              ))}
            </select>
          </div>

          <div className={styles.buttonGroup}>
             <Button type="submit">Search</Button>
          </div>

        </div>
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