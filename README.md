# ArcGIS Desktop Python Tools
A collection of custom Esri toolboxes written in python.

## Geodatabase toolbox
Tools for handling with geodatabase maintenance and conversion tasks.

### Clip geodatabase
This tool clips each layer in a geodatabase and projects the data into an output database using a specified projection file.

### Reproject geodatabase
Reprojects an entire geodatabase using a specified projection file. Layers not in a dataset will be placed in a `_top` dataset.

## Mapping toolbox
ArcMap mapping tools to be used in an open MXD document

### Generate Site Maps and CSV
A custom data driven pages tool used for a variety of purposes.
- Optionally buffers selected feature or features
- Selects features that intersect the buffer
- Exports map of all features
- Optionally exports individual data driven pages for each feature
- Exports a csv file with the selected features
