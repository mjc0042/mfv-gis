import geopandas as gpd

from scripts.db_connection import get_engine
from scripts.utils import get_numeric_value

TARGET_CRS = "EPSG:4269"

def transform_ny_row(row):
    return {
        "id": int(row.get("FIPS_CODE")),
        "municipal_name": row["NAME"].title() if row["NAME"] else "",
        "municipal_code": str(row["MUNITYCODE"]) if row.get("MUNITYCODE") else "",
        "municipal_type": row["MUNI_TYPE"].title() if row.get("MUNI_TYPE") else "",
        "county_name": row["COUNTY"].title() if row.get("COUNTY") else "",
        "state": "NY",
        "gnis_id": str(row.get("GNIS_ID")) if row.get("GNIS_ID") else None,
        "fips_code": row.get("FIPS_CODE", ""),
        "fips_name": row["NAME"].title() if row.get("NAME") else "",
        "pop_1990": get_numeric_value(row.get("POP1990")),
        "pop_2000": get_numeric_value(row.get("POP2000")),
        "pop_2010": get_numeric_value(row.get("POP2010")),
        "pop_2020": get_numeric_value(row.get("POP2020")),
        "sq_mi": get_numeric_value(row.get("CALC_SQ_MI")),
        "geometry": row.geometry
    }

def load_ny_gdb_to_postgres(gdb_path, layer_name, table_name):
    # Read GIS data and convert to target CRS
    gdf = gpd.read_file(gdb_path, layer=layer_name)
    gdf = gdf.to_crs(TARGET_CRS)

    # Transform data
    transformed_rows = gdf.apply(transform_ny_row, axis=1, result_type='expand')
    
    # Create new GeoDataFrame with transformed data
    new_gdf = gpd.GeoDataFrame(transformed_rows, geometry='geometry', crs=gdf.crs)

    engine = get_engine()
    new_gdf.to_postgis(table_name, engine, if_exists='replace', index=False)

    print(f"NY data loaded into table {table_name} as CRS {gdf.crs}.")

def main():
    load_ny_gdb_to_postgres(
        gdb_path="data/NYS_Civil_Boundaries.gdb",
        layer_name="Cities_Towns",
        table_name="municipal_boundaries"
    )

if __name__ == "__main__":
    main()

