import geopandas as gpd

from scripts.db_connection import get_engine
from scripts.utils import get_numeric_value

TARGET_CRS = "EPSG:4269"

def transform_pa_row(pa_record: dict) -> dict:
    """
    Transform a PA municipal record dict to unified schema dict.
    Assume pa_record keys as specified (e.g. 'MUNICIPAL_NAME', 'MUNICIPAL_CODE', etc.)
    """
    fips_code = f"{pa_record.get('FIPS_STATE', '')}{pa_record.get('FIPS_COUNTY_CODE', '')}{pa_record.get('FIPS_MUN_CODE', '')}"
    return {
        "id": int(fips_code),
        "municipal_name": pa_record.get("MUNICIPAL_NAME", "").title(),
        "municipal_code": str(pa_record.get("MUNICIPAL_CODE", "")).strip(),
        "municipal_type": decode_pa_municip_type(pa_record.get("CLASS_OF_MUNIC")) if pa_record.get("CLASS_OF_MUNIC") is not None else "",  # custom function to decode codes like '2TWP'
        "county_name": pa_record.get("COUNTY_NAME", "").title(),
        "state": "PA",
        "gnis_id": str(pa_record.get("GNIS_PPL", "")).replace(",", ""),
        "fips_code": fips_code,
        "fips_name": pa_record.get("FIPS_AREA_NAME", "").title() if pa_record.get("FIPS_AREA_NAME", "") is not None else "",
        "pop_1990": None,  # PA example has no 1990 pop
        "pop_2000": None,  # PA example has no 2000 pop
        "pop_2010": get_numeric_value(pa_record.get("FIPS_MUN_POP_2010")),
        "pop_2020": get_numeric_value(pa_record.get("FIPS_MUN_POP_2020")),
        "sq_mi": get_numeric_value(pa_record.get("FIPS_SQ_MI")),
        "geometry": pa_record.geometry
    }

def decode_pa_municip_type(code: str) -> str:
    # Map PA municipality codes to readable types 
    # Example: '2TWP' => 'Township'
    if not code:
        return "Unknown"
    if "TWP" in code:
        return "Township"
    if "BOR" in code:
        return "Borough"
    if "CITY" in code or "CIT" in code:
        return "City"
    return code  # fallback


def load_pa_geojson_to_postgres(geojson_path, table_name):
    # Read GIS data and convert to target CRS
    gdf = gpd.read_file(geojson_path)
    gdf = gdf.to_crs(TARGET_CRS)

    # Transform data
    transformed_rows = gdf.apply(transform_pa_row, axis=1, result_type='expand')

    # Create new GeoDataFrame with transformed data, keep geometry
    new_gdf = gpd.GeoDataFrame(transformed_rows, geometry='geometry', crs=gdf.crs)

    engine = get_engine() 
    new_gdf.to_postgis(table_name, engine, if_exists='replace', index=False)

    print(f"PA data loaded into table {table_name} as CRS {gdf.crs}.")

def main():
    load_pa_geojson_to_postgres(
        geojson_path="data/Pennsylvania_Municipality_Boundary.geojson",
        table_name="municipal_boundaries"
    )

if __name__ == "__main__":
    main()

