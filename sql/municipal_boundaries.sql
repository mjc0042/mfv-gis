-- Enable PostGIS extension if not already enabled
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create unified municipalities table
CREATE TABLE municipal_boundaries (
    id INTEGER PRIMARY KEY,
    municipal_name TEXT NOT NULL,
    municipal_code TEXT,
    municipal_type TEXT,
    county_name TEXT,
    state CHAR(2) NOT NULL, -- e.g. 'PA', 'NY'
    gnis_id TEXT,
    fips_code TEXT NOT NULL,
    fips_name TEXT,
    pop_1990 INTEGER,
    pop_2000 INTEGER,
    pop_2010 INTEGER,
    pop_2020 INTEGER,
    sq_mi DOUBLE PRECISION,
    geometry GEOMETRY(MultiPolygon, 4269) -- assuming NAD83 projection
);

-- Create spatial index on geometry for fast spatial queries
CREATE INDEX idx_municipal_boundaries_geom ON municipal_boundaries USING GIST (geometry);

-- Optional: Indexes to speed up queries on commonly filtered columns
CREATE INDEX idx_municipal_boundaries_by_state ON municipal_boundaries (state);
CREATE INDEX idx_municipal_boundaries_by_county_name ON municipal_boundaries (county_name);
CREATE INDEX idx_municipal_boundaries_by_municipal_name ON municipal_boundaries (municipal_name);
