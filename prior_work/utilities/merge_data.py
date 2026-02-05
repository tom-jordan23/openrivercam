#!/usr/bin/env python3
import pandas as pd
from datetime import datetime
import numpy as np

def convert_depth_timestamp(timestamp_ms):
    """Convert Unix timestamp in milliseconds to datetime"""
    # Depth timestamps appear to be 3 hours ahead of CDT
    dt = pd.to_datetime(timestamp_ms, unit='ms')
    # Subtract 3 hours to align with location data (CDT)
    return dt - pd.Timedelta(hours=3)

def convert_location_timestamp(time_str):
    """Convert location timestamp string to datetime"""
    # Remove timezone info and parse
    cleaned_time = pd.Series(time_str).str.replace(r' [A-Z]{3}$', '', regex=True)
    return pd.to_datetime(cleaned_time)

def merge_depth_location_data():
    # Read depth data
    print("Reading depth.csv...")
    depth_df = pd.read_csv('depth.csv')
    depth_df = depth_df.dropna(subset=['time'])  # Remove rows with NaN timestamps
    depth_df['datetime'] = convert_depth_timestamp(depth_df['time'])
    depth_df['timestamp_second'] = depth_df['datetime'].dt.floor('s')
    
    # Read location data
    print("Reading location.csv...")
    location_df = pd.read_csv('location.csv')
    location_df = location_df.dropna(subset=['Time'])  # Remove rows with NaN timestamps
    location_df['datetime'] = convert_location_timestamp(location_df['Time'])
    location_df['timestamp_second'] = location_df['datetime'].dt.floor('s')
    
    # Average depth data by second
    print("Averaging depth data by second...")
    depth_averaged = depth_df.groupby('timestamp_second').agg({
        'depth': 'mean',
        'temperature': 'mean',
        'latitude': 'mean',
        'longtitude': 'mean'
    }).reset_index()
    depth_averaged = depth_averaged.rename(columns={'longtitude': 'longitude'})
    
    # Average location data by second
    print("Averaging location data by second...")
    location_averaged = location_df.groupby('timestamp_second').agg({
        'Lat': 'mean',
        'Lon': 'mean',
        'Elevation': 'mean',
        'Speed': 'mean',
        'Bearing': 'mean',
        'Horizontal Accuracy': 'mean',
        'Vertical Accuracy': 'mean'
    }).reset_index()
    
    # Merge the datasets on timestamp_second
    print("Merging datasets...")
    merged_df = pd.merge(depth_averaged, location_averaged, on='timestamp_second', how='outer')
    
    # Sort by timestamp
    merged_df = merged_df.sort_values('timestamp_second')
    
    # Create QGIS-compatible columns
    # Use location data coordinates as primary, fallback to depth data if available
    merged_df['longitude'] = merged_df['Lon'].fillna(merged_df.get('longitude', np.nan))
    merged_df['latitude'] = merged_df['Lat'].fillna(merged_df.get('latitude', np.nan))
    
    # Reorder columns for QGIS compatibility (longitude, latitude first)
    columns_order = [
        'longitude',
        'latitude', 
        'timestamp_second', 
        'depth', 
        'temperature',
        'Elevation',
        'Speed',
        'Bearing',
        'Horizontal Accuracy',
        'Vertical Accuracy'
    ]
    
    # Only include columns that exist and have coordinate data
    existing_columns = [col for col in columns_order if col in merged_df.columns]
    merged_df = merged_df[existing_columns]
    
    # Remove rows without coordinate data (required for QGIS)
    merged_df = merged_df.dropna(subset=['longitude', 'latitude'])
    
    # Write to combined.csv
    print("Writing to combined.csv...")
    merged_df.to_csv('combined.csv', index=False)
    
    print(f"Successfully merged data. Output contains {len(merged_df)} rows.")
    print(f"Time range: {merged_df['timestamp_second'].min()} to {merged_df['timestamp_second'].max()}")
    
    return merged_df

if __name__ == "__main__":
    merged_data = merge_depth_location_data()
    print("\nFirst 5 rows of merged data:")
    print(merged_data.head())