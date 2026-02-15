export interface Movie {
  tmdb_id: number;
  title: string;
  poster_path: string;
  backdrop_path?: string;
  release_date: string;
  overview: string;
  cast?: string[]; // Simplified for this demo
}

export interface Rating {
  score: number;
  movie_id: number;
}

// Combines movie data with the user's personal rating
export interface RatedMovie extends Movie {
  userRating?: number;
}

export interface User {
  email: string;
  token: string;
}

export interface Genre {
  id: number;
  name: string;
}
