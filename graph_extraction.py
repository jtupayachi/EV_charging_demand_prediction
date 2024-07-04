import osmnx as ox
import pandas as pd

df = pd.read_csv('california_charge_selected.csv') #use your own file location
print('California: \n', df)
cols = df.columns
print(cols)

'''The following function will return individual station-level graph (ie.e., only POI information for our project) information which will be later feed to GNN model'''
def graph_extraction(latitude, longitude, distance_in_meters):
    # Create a bounding box around the specified station location
    north, south, east, west = ox.utils_geo.bbox_from_point((latitude, longitude), dist=distance_in_meters)
    tags = {'amenity': True}
    features_gdf = ox.geometries_from_bbox(north, south, east, west, tags)
    features_gdf = features_gdf[features_gdf['geometry'].type == 'Point'][['amenity', 'geometry']]
    features_gdf.reset_index(inplace=True)
    features_gdf['latitude'] = features_gdf['geometry'].y
    features_gdf['longitude'] = features_gdf['geometry'].x
    features_gdf.drop(columns=['element_type', 'osmid', 'geometry'], inplace=True)
    return features_gdf

for index, row in df.iterrows():
    amenities_df = graph_extraction(row['Latitude'], row['Longitude'], 804.7)
    print(amenities_df.head())
    amenities_cols = amenities_df.columns
    print(amenities_cols)
    











