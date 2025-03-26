from mapping.folium_map import *
import yaml

def main():
    """
    Produce all required map iframes
    """
    # Load config
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    # Loop through required years
    for i in range(2014, 2025):
        file_extension = str(i)

        # Create map
        geo_df = create_gdf(i)
        m = generate_map_from_gdf(geo_df, w=config["width"], h=config["height"])

        # Serve map to iframe
        m.get_root().width = config["width_px"]
        m.get_root().height = config["height_px"]
        iframe = m.get_root()._repr_html_()

        # Write out iframe to HTML
        filename = f"map_{file_extension}.html"
        html_file = open(f"static/{filename}", "w")
        html_file.write(iframe)
        html_file.close
    
if __name__ == "__main__":
    main()