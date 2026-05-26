import argparse
from . import map_loader

def main():
    parser = argparse.ArgumentParser(description="Download and load Natural Earth data.")
    parser.add_argument("category", choices=["cultural", "physical"], help="Data category")
    parser.add_argument("name", help="Dataset name (e.g., admin_0_countries)")
    parser.add_argument("--res", default="10m", help="Resolution (default: 10m)")
    parser.add_argument("--out", help="Output file to save as GeoJSON (optional)")
    args = parser.parse_args()

    gdf = map_loader.get_natural_earth(args.category, args.name, args.res)
    if args.out:
        gdf.to_file(args.out, driver="GeoJSON")
        print(f"Saved to {args.out}")
    else:
        print(gdf.head())

if __name__ == "__main__":
    main()
