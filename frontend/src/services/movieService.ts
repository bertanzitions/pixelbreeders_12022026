import { Movie } from '../types';

const API_URL = process.env.REACT_APP_API_URL;

// Helper to handle responses and auth errors
const handleResponse = async (res: Response, logout: () => void) => {
  const data = await res.json();
  if (res.status === 401 || res.status === 422) {
    if (data.msg === "Token has expired") {
      alert("Your session has expired. Please login again.");
      logout();
      throw new Error("Session expired");
    }
  }
  if (!res.ok) throw new Error(data.error || "API Error");
  return data;
};

const getHeaders = (token: string) => ({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token}`
});

export const movieService = {
  getRatedMovies: async (token: string, logout: () => void) => {
    const res = await fetch(`${API_URL}/reviews/ratings`, { headers: getHeaders(token) });
    return handleResponse(res, logout);
  },

  searchMovies: async (query: string, page: number, year?: string, genre?: string) => {
    let url = `${API_URL}/movies/search?query=${encodeURIComponent(query)}&page=${page}`;
    if (year) url += `&year=${year}`;
    if (genre) url += `&genre=${genre}`;
    
    const res = await fetch(url, { headers: { 'Content-Type': 'application/json' } });
    return res.json();
  },
  
  rateMovie: async (token: string, movie: Movie, score: number, isUpdate: boolean, logout: () => void) => {
    const method = isUpdate ? 'PUT' : 'POST';
    const url = isUpdate 
      ? `${API_URL}/reviews/ratings/${movie.tmdb_id}` 
      : `${API_URL}/reviews/ratings`;

    const payload: any = { score };
    if (!isUpdate) {
      payload.tmdb_id = movie.tmdb_id;
      payload.movie_data = {
        title: movie.title,
        poster_path: movie.poster_path,
        backdrop_path: movie.backdrop_path,
        overview: movie.overview,
        release_date: movie.release_date
      };
    }

    const res = await fetch(url, {
      method,
      headers: getHeaders(token),
      body: JSON.stringify(payload)
    });
    return handleResponse(res, logout);
  },

  deleteRating: async (token: string, tmdb_id: number, logout: () => void) => {
    const res = await fetch(`${API_URL}/reviews/ratings/${tmdb_id}`, {
      method: 'DELETE',
      headers: getHeaders(token)
    });
    return handleResponse(res, logout);
  },

  getGenres: async () => {
    const res = await fetch(`${API_URL}/genres`);
    if (!res.ok) throw new Error('Failed to fetch genres');
    return res.json(); // Returns Genre[]
  },

  
};