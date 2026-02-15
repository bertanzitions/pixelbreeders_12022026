import React from 'react';
import { useDashboard } from '../../hooks/useDashboard';
import Navbar from '../../components/general/NavBar';
import MovieModal from '../../components/search/MovieModal';
import SearchSection from '../../components/dashboard/SearchSection';
import ReviewedSection from '../../components/dashboard/ReviewedSection';

const Dashboard = () => {
  const {
    currentView,
    setCurrentView,
    selectedMovie,
    query,
    setQuery,
    searchResults,
    reviewedMovies,
    isLoading,
    handleSearchFormSubmit,
    handleRateMovie,
    handleDeleteRating,
    openModal,
    closeModal,
    lastMovieElementRef
  } = useDashboard();

  return (
    <div className="app-container">
      <Navbar currentView={currentView} setView={setCurrentView} />

      {currentView === 'search' ? (
        <SearchSection 
          query={query}
          setQuery={setQuery}
          onSubmit={handleSearchFormSubmit}
          results={searchResults}
          lastElementRef={lastMovieElementRef}
          onMovieClick={openModal}
          isLoading={isLoading}
        />
      ) : (
        <ReviewedSection 
          movies={reviewedMovies}
          onMovieClick={openModal}
        />
      )}

      {selectedMovie && (
        <MovieModal 
          movie={selectedMovie} 
          onClose={closeModal} 
          onRate={handleRateMovie} 
          onDelete={handleDeleteRating}
        />
      )}
    </div>
  );
};

export default Dashboard;