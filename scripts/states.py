import geopandas as gpd

from scripts.db_connection import get_engine

TARGET_CRS = "EPSG:4269" #NAD83

def load_data_to_postgres(file_path, table_name):
    # Read GIS data and convert to target CRS
    gdf = gpd.read_file(file_path)

    if (gdf.crs != TARGET_CRS):
        gdf = gdf.to_crs(TARGET_CRS)

    # Convert all column names to lowercase
    gdf.columns = gdf.columns.str.lower()

    # Add ID field based on state FIPS code
    gdf["id"] = gdf["statefp"].astype(int)

    engine = get_engine() 
    gdf.to_postgis(table_name, engine, if_exists='replace', index=False)

    print(f"State outlines loaded into table {table_name} as CRS {gdf.crs}.")

def main():
    load_data_to_postgres(
        file_path="data/state_boundaries/cb_2024_us_state_5m.shp",
        table_name="state_boundaries"
    )

if __name__ == "__main__":
    main()

