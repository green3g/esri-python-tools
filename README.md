# ArcGIS Desktop Python Tools
A collection of custom Esri toolboxes written in python.

## Utilities toolbox
ArcGIS Utilities

### Generate Site Maps and CSV
A custom data driven pages tool used for a variety of purposes.
- Optionally buffers selected feature or features
- Selects features that intersect the buffer
- Exports map of all features
- Optionally exports individual data driven pages for each feature
- Exports a csv file with the selected features

### Clip geodatabase
This tool clips each layer in a geodatabase and projects the data into an output database using a specified projection file.

### Reproject geodatabase
Reprojects an entire geodatabase using a specified projection file. Layers not in a dataset will be placed in a `_top` dataset.

### Polygon Centroid Tool
 - Copies a polygon feature class's centroid geometry into a new feature class
 - Adds field `Rel_OID` type `Long` which represents the object id of the polygon

### Line Endpoint Tool
![screenshot](img/line_endpoint.PNG)
 - Copies the start and endpoint of lines into a new feature class
 - Adds field `related_oid` type `Long` which represents the object id of the line feature
 - Adds field `point_type` type `Text` which will either be value `START` or `END`
 - See http://pro.arcgis.com/en/pro-app/arcpy/classes/geometry.htm

### Point Elevation Tool
 - Extracts elevation values at points and calculates them to a field
 - This may crash ArcMap with large data sets

## Scripts

### Calculate Dynamic Expression Related Records
Calculates the dynamic expression for a layer and can be used to dynamically
display related records text for data driven pages or feature labels

#### Usage (see script for detail)
 - Change the FindLabel parameter to the id field of the main table
 - This id should be related to each of the related tables
 - Also change the first line of FindLabel. Set parameter equal to the FindLabel parameter
 - Change the lookup tables and assign their appropriate formatter function
