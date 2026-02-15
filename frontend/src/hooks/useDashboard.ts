import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { Movie, RatedMovie, Genre } from '../types'; // Import Genre
import { movieService } from '../services/movieService';
import { useInfiniteScroll } from './useInfiniteScroll';

export const useDashboard = () => {
  const { user, logout } = useAuth();
  
  // UI State
  const [currentView, setCurrentView] = useState<'search' | 'reviewed'>('search');
  const [selectedMovie, setSelectedMovie] = useState<RatedMovie | null>(null);

  // Search & Filter State
  const [query, setQuery] = useState('');
  const [year, setYear] = useState('');       // NEW
  const [genre, setGenre] = useState('');     // NEW (stores the ID)
  const [genresList, setGenresList] = useState<Genre[]>([]); // NEW (stores list for dropdown)

  const [searchResults, setSearchResults] = useState<Movie[]>([]);
  const [reviewedMovies, setReviewedMovies] = useState<RatedMovie[]>([]);
  
  // Pagination State
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch the list of genres when the hook loads
  useEffect(() => {
    const loadGenres = async () => {
      try {
        const list = await movieService.getGenres();
        setGenresList(list);
      } catch (error) {
        console.error("Failed to load genres", error);
      }
    };
    loadGenres();
  }, []);

  // --- ACTIONS ---

  const fetchReviewedMovies = useCallback(async () => {
    if (!user?.token) return;
    try {
      const data = await movieService.getRatedMovies(user.token, logout);
      const formatted = data.map((item: any) => ({
        ...item.movie,
        userRating: item.movie.rating
      }));
      setReviewedMovies(formatted);
    } catch (error) {
      console.error("Failed to fetch reviews", error);
    }
  }, [user?.token, logout]);

  // Updated search to include filters
  const performSearch = useCallback(async (pageNum: number, isNewSearch: boolean) => {
    if (!query.trim()) return;
    setIsLoading(true);

    try {
      // Pass query, page, year, and genre ID to service
      const data = await movieService.searchMovies(query, pageNum, year, genre);
      if (data.results) {
        setTotalPages(data.total_pages);
        setSearchResults(prev => isNewSearch ? data.results : [...prev, ...data.results]);
      }
    } catch (error) {
      console.error("Search error:", error);
    } finally {
      setIsLoading(false);
    }
  }, [query, year, genre]); // Dependencies include filters

  const handleRateMovie = async (score: number) => {
    if (!selectedMovie || !user?.token) return;
    try {
      const isUpdate = !!selectedMovie.userRating;
      await movieService.rateMovie(user.token, selectedMovie, score, isUpdate, logout);
      setSelectedMovie({ ...selectedMovie, userRating: score });
      if (currentView === 'reviewed') fetchReviewedMovies();
    } catch (error) {
      console.error("Rate movie error", error);
    }
  };

  const handleDeleteRating = async () => {
    if (!selectedMovie || !user?.token) return;
    try {
      await movieService.deleteRating(user.token, selectedMovie.tmdb_id, logout);
      const movieReset = { ...selectedMovie };
      delete movieReset.userRating;
      setSelectedMovie(movieReset);
      if (currentView === 'reviewed') {
        setReviewedMovies(prev => prev.filter(m => m.tmdb_id !== selectedMovie.tmdb_id));
      }
    } catch (error) {
      console.error("Delete rating error", error);
    }
  };

  // Handlers
  const handleSearchFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchReviewedMovies();
    setPage(1);
    setSearchResults([]);
    setTotalPages(0);
    performSearch(1, true);
  };

  const openModal = (movie: Movie) => {
    const existing = reviewedMovies.find(r => String(r.tmdb_id) === String(movie.tmdb_id));
    setSelectedMovie(existing || { ...movie });
  };

  const closeModal = () => setSelectedMovie(null);

  // Observers / Effects
  const lastMovieElementRef = useInfiniteScroll(
    isLoading, 
    page < totalPages, 
    () => setPage(prev => prev + 1)
  );

  useEffect(() => {
    if (currentView === 'reviewed') fetchReviewedMovies();
  }, [currentView, fetchReviewedMovies]);

  useEffect(() => {
    if (page > 1) performSearch(page, false);
  }, [page, performSearch]);

  return {
    currentView, setCurrentView,
    selectedMovie, openModal, closeModal,
    query, setQuery,
    year, setYear,
    genre, setGenre,
    genresList,
    searchResults, reviewedMovies,
    isLoading,
    handleSearchFormSubmit,
    handleRateMovie,
    handleDeleteRating,
    lastMovieElementRef
  };
};