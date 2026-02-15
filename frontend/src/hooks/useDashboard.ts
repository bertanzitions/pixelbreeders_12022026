import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { Movie, RatedMovie } from '../types';
import { movieService } from '../services/movieService';
import { useInfiniteScroll } from './useInfiniteScroll';

export const useDashboard = () => {
  const { user, logout } = useAuth();
  
  // UI State
  const [currentView, setCurrentView] = useState<'search' | 'reviewed'>('search');
  const [selectedMovie, setSelectedMovie] = useState<RatedMovie | null>(null);

  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Movie[]>([]);
  const [reviewedMovies, setReviewedMovies] = useState<RatedMovie[]>([]);
  
  // page state
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  // --- ACTIONS ---

  const fetchReviewedMovies = useCallback(async () => {
    if (!user?.token) return;
    try {
      const data = await movieService.getRatedMovies(user.token, logout);
      
      // API response to front end model
      const formatted = data.map((item: any) => ({
        ...item.movie,
        userRating: item.movie.rating
      }));
      setReviewedMovies(formatted);
    } catch (error) {
      console.error("Failed to fetch reviews", error);
    }
  }, [user?.token, logout]);

  const performSearch = useCallback(async (pageNum: number, isNewSearch: boolean) => {
    if (!query.trim()) return;
    setIsLoading(true);

    try {
      const data = await movieService.searchMovies(query, pageNum);
      if (data.results) {
        setTotalPages(data.total_pages);
        setSearchResults(prev => isNewSearch ? data.results : [...prev, ...data.results]);
      }
    } catch (error) {
      console.error("Search error:", error);
    } finally {
      setIsLoading(false);
    }
  }, [query]);

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
      
      // Optimistic UI Update
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

  // handlers
  const handleSearchFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // updates it every time that it is searched so that
    // no review movie is left behind
    fetchReviewedMovies();
    
    setPage(1);
    setSearchResults([]);
    setTotalPages(0);
    performSearch(1, true);
  };

  const openModal = (movie: Movie) => {

    // HAS TO BE STRING!!
    console.log(movie)
    const existing = reviewedMovies.find(r => 
        String(r.tmdb_id) === String(movie.tmdb_id)
    );
    
    if (existing) {
        setSelectedMovie(existing);
    } else {
        setSelectedMovie({ ...movie });
    }
};

  const closeModal = () => setSelectedMovie(null);

  // OBSERVERS / EFFECTS
  // hook for infinite scroll
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
    searchResults, reviewedMovies,
    isLoading,
    handleSearchFormSubmit,
    handleRateMovie,
    handleDeleteRating,
    lastMovieElementRef
  };
};