# Creating a Depth Heatmap in QGIS

This guide walks you through importing the combined depth and location data into QGIS and creating a heatmap visualization with an OpenStreetMap background.

## Prerequisites
- QGIS installed (version 3.x recommended)
- `combined.csv` file generated from the merge script

## Step 1: Import the CSV Data into QGIS

1. **Open QGIS** and create a new project
2. **Add the CSV layer:**
   - Go to `Layer` → `Add Layer` → `Add Delimited Text Layer...`
   - Or click the "Add Delimited Text Layer" icon in the toolbar
3. **Configure the import:**
   - **File name:** Browse and select `combined.csv`
   - **File format:** Select "CSV (comma separated values)"
   - **Geometry definition:** Choose "Point coordinates"
   - **X field:** Select `longitude`
   - **Y field:** Select `latitude`
   - **Geometry CRS:** Set to `EPSG:4326 - WGS 84`
4. **Click "Add"** then **"Close"**

## Step 2: Add OpenStreetMap Background

1. **Open the Browser Panel** (View → Panels → Browser if not visible)
2. **Navigate to XYZ Tiles:**
   - In the Browser panel, expand "XYZ Tiles"
   - Double-click on "OpenStreetMap" to add it as a base layer
3. **Reorder layers:**
   - In the Layers panel, drag the OpenStreetMap layer below your CSV layer
   - This ensures the points appear on top of the map

## Step 3: Create a Heatmap

1. **Right-click on your CSV layer** in the Layers panel
2. **Select "Properties"**
3. **Go to the "Symbology" tab**
4. **Change the symbology type:**
   - At the top, change the dropdown from "Single Symbol" to "Heatmap"
5. **Configure heatmap settings:**
   - **Radius:** Set to approximately 20-50 pixels (adjust based on your data density)
   - **Maximum value:** Leave as "Automatic" or set manually based on your depth range
   - **Color ramp:** Choose an appropriate color scheme (e.g., "Viridis" or "Spectral")
   - **Weight points by:** Select `depth` from the dropdown
6. **Adjust rendering quality:**
   - **Render quality:** Set to "Best" for final output
7. **Click "OK"** to apply the heatmap

## Step 4: Fine-tune the Visualization

1. **Adjust the color ramp:**
   - Return to Layer Properties → Symbology
   - Click on the color ramp to modify colors
   - Consider inverting the ramp if deeper areas should be "cooler" colors
2. **Modify radius and opacity:**
   - Experiment with different radius values (10-100 pixels)
   - Adjust layer opacity in the Layers panel if needed
3. **Set map extent:**
   - Right-click your data layer → "Zoom to Layer"
   - This centers the view on your data points

## Step 5: Enhance the Map (Optional)

1. **Add a legend:**
   - Go to `Project` → `New Print Layout`
   - Add a legend: `Insert` → `Add Legend`
   - Configure legend properties to show depth values
2. **Add labels or additional styling:**
   - Consider adding a title and scale bar
   - Adjust the overall color scheme for better contrast with the OSM background

## Step 6: Export the Map

1. **For a quick export:**
   - Go to `Project` → `Import/Export` → `Export Map to Image...`
   - Choose resolution and file format
2. **For a professional layout:**
   - Use the Print Layout created in Step 5
   - Export as PDF or high-resolution image

## Troubleshooting

- **Points not visible:** Check that the CRS is set correctly (EPSG:4326)
- **Heatmap too sparse:** Decrease the radius value
- **Heatmap too dense:** Increase the radius value
- **Colors not representing depth well:** Try different color ramps or invert the current one
- **Map projection issues:** Ensure both layers use the same CRS

## Additional Tips

- Use the "Identify Features" tool to inspect individual data points
- Consider filtering data by depth ranges using the "Filter" option in layer properties
- For large datasets, you may want to create different heatmaps for different depth ranges
- Save your project (.qgz file) to preserve all settings for future use