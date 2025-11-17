CREATE TABLE citations (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  citation_type TEXT NOT NULL,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  journal TEXT NOT NULL,
  year INTEGER NOT NULL,
  volume FLOAT NOT NULL,
  number INTEGER NOT NULL,
  pages TEXT NOT NULL
);
