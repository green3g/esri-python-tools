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

## Scripts

### Calculate Dynamic Expression Related Records
Calculates the dynamic expression for a layer and can be used to dynamically
display related records text for data driven pages or feature labels

#### Usage (see script for detail)
 - Change the FindLabel parameter to the id field of the main table
 - This id should be related to each of the related tables
 - Also change the first line of FindLabel. Set parameter equal to the FindLabel parameter
 - Change the lookup tables and assign their appropriate formatter function
