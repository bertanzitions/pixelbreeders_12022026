import React from 'react';
import { RatedMovie } from '../../types';

interface MovieModalProps {
  movie: RatedMovie;
  onClose: () => void;
  onRate: (score: number) => void;
  onDelete: () => void;
}

const MovieModal: React.FC<MovieModalProps> = ({ movie, onClose, onRate, onDelete }) => {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>X</button>

        <h2>{movie.title}</h2>

        {movie.backdrop_path && (
          <img
            src={`https://image.tmdb.org/t/p/w500${movie.backdrop_path}`}
            alt="Backdrop"
            style={{ width: '100%', borderRadius: '4px', marginBottom: '10px' }}
          />
        )}

        <p><strong>Release Date:</strong> {movie.release_date || 'Unknown'}</p>
        <p>{movie.overview || 'No synopsis available.'}</p>

        <div className="rating-section">
          <h4>Evaluation</h4>
          <div className="rating-controls">
            {[1, 2, 3, 4, 5].map((num) => (
              <button
                key={num}
                onClick={() => onRate(num)}
                style={{
                  fontWeight: movie.userRating === num ? 'bold' : 'normal',
                  background: movie.userRating === num ? '#ddd' : 'white',
                  border: '1px solid black',
                  padding: '5px 10px',
                  cursor: 'pointer',
                }}
              >
                {num}
              </button>
            ))}
          </div>
          {movie.userRating && (
            <button
              onClick={onDelete}
              style={{ marginTop: '10px', color: 'red', background: 'none', border: 'none', cursor: 'pointer', textDecoration: 'underline' }}
            >
              Remove Rating
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default MovieModal;