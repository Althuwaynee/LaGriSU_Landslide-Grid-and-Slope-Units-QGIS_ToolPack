# LaGriSU_Landslide-Grid-and-Slope-Units-QGIS_ToolPack

LaGriSU v 0.2 (Landslide Grid and Slope Units): binary (1,0) samples extraction tool pack, used for landslides mapping.
The tool developed in QGIS proccessing tools using SAGA and GDAL libraries.
LaGriSU works both in windows and other operating systems.

The tool mainly based on the concept of the drainage network (i.e., the valley line) that is extracted from the original DEM data in order to generate the catchment basin in positive relief through the hydrological analysis module in QGIS.
Previous version (version 1) was published on GitHub in August 2018, and the current version 2 (2022) comes with enhanced performance in term of pc resources and QGIS new versions.



..........


**Omar F. AlThuwaynee**, *Developer* 

*GIS and Geomatics (Geo-Informatics) Engineering, PhD.*
*Scientists Adoption Academy (scadacademy.com)*
*Editorial Board: Landslides*
*ORCID: 0000-00019863-2046*

## Installation

Tool pack modules built of graphical modeler of QGIS [versions](https://qgis.org/downloads/) 3.4.0, 3.6.0 and 3.8.0.

..1.	Go to Settings > Options > Processing and under General change to Ignore features with invalid geometries...
..2.	Unzip tool pack to the QGIS library..


### In order to view the tool pack
we must download the supplied folder (Models) to the “processing” folder inside the QGIS root folder, as follow:
Open QGIS, go to processing > Copy the provided “model” folder> Models icon (red Engine) and choose Open existing model > paste provided “model” folder and replace with existing one.


![Screenshot_4](https://user-images.githubusercontent.com/8848123/155887780-8a904439-bce4-4fb4-9160-fbcab6b8f9ce.png)


### Required input:
•	Landslide locations with points OR polygons features
•	DEM raster
### Intro about the LaGriSU 2022 updates

Link to video:  https://youtu.be/oim-dyc7haE

![su](https://user-images.githubusercontent.com/8848123/155884250-fa01a054-7032-4651-a77c-0a5c72d8b785.jpg)

![20221003_113703](https://user-images.githubusercontent.com/8848123/202452164-488f69cb-420e-42ae-ba0d-1b895e9d7c2d.jpg)


