-- Enable PostGIS extension if not already enabled
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create the state_boundaries table
CREATE TABLE public.state_boundaries (
    id INTEGER PRIMARY KEY,
    statefp TEXT,
    statens TEXT,
    geoidfq TEXT,
    geoid TEXT,
    stusps TEXT,
    name TEXT,
    lsad TEXT,
    aland BIGINT,
    awater BIGINT,
    geometry GEOMETRY(MULTIPOLYGON, 4269) --  NAD83
);

-- Create spatial index on geometry to speed up spatial queries
CREATE INDEX idx_state_boundaries_geom ON public.state_boundaries USING GIST (geometry);
