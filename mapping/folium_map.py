import folium
import geopandas
import json
from mapping.prep_data import *

def create_gdf(period: int):
    """
    Function to create a GeoPandas DataFrame from the spatial data file 
    and then merge feature data into it
    # Todo: Control for inflation on wage data
    """

    # Get feature data
    lad_df = get_df_from_db()

    # Data cleaning
    lad_df_filtered = lad_df[lad_df["year"]==period]
    lad_df_filtered = lad_df_filtered.dropna()
    lad_df_filtered["median_ann_pay"] = lad_df_filtered["median_ann_pay"].astype("int64")

    # Get spatial data
    gdf = geopandas.read_file("data/local_authority_district_boundaries.geojson")

    # Join feature data on spatial data
    gdf = gdf.merge(
        lad_df_filtered,
        how="left",
        left_on="LAD24NM",
        right_on="lad"
    )

    return gdf

def generate_map_from_gdf(gdf, w, h):
    """
    Generate a folium map from the supplied GeoPandas DataFrame
    """

    m = folium.Map(
        location=[53.5,  -2.2],
        width=w,
        height=h,
        zoom_start=6,
        min_zoom=6,
        tiles=None
    )

    folium.Choropleth(
        geo_data=gdf,
        data=gdf,
        columns=["lad", "median_ann_pay"],
        key_on="properties.LAD24NM",
        nan_fill_color="purple",
        nan_fill_opacity=0.4,
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Median Gross Annual Pay (£)",
        highlight=True
    ).add_to(m)

    return m