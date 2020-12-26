# LaGriSU_Landslide-Grid-and-Slope-Units-QGIS_ToolPack

LaGriSU v 0.2 (Landslide Grid and Slope Units): binary (1,0) samples extraction tool pack for landslides mapping in QGIS

**Omar F. AlThuwaynee**, *Developer* 

## Introduction
* LaGriSU, designed specifically for landslide mapping  applications,  developed in QGIS tool box modeler, The  Tool  Pack  does not requires  an  internet  connection or Java runtime environment at any stage (just copy and paste the modules in models library).
* The first version of QGIS.GSU V.01 was released in 2018, presented in online course “” as part of landslide susceptibility mapping tutorials. Since that time, 200 user was download and used the tool, and that let us collect all the complains, bugs, workability issues to be fix in the current V0.2.
* Tool provided a user-friendly experience to systematically learn (open box), visualize and validate the extracted samples stored in many different resultant layers (before and after to be merged), and to update the extracted samples whenever the features homogeneity was disturbed. 
* Furthermore, the tool does not need any programing or advance GIS skills to be executed.

To check the Tool version 0.1, please visit the [Udemy course](https://www.udemy.com/course/susceptibility-auto-mapping-tools-for-trainingtesting-data/)


## News

* Please follow up with updates about the tools by visiting Issues button


## Technical requirements and software compatibility

Tool pack modules built of graphical modeler of QGIS [versions](https://qgis.org/downloads/) 3.4.0, 3.6.0 and 3.8.0.

1.	Go to Settings > Options > Processing and under General change to Ignore features with invalid geometries.
2.	Unzip tool pack to the QGIS library

### In order to view the tool pack
we must unzip the supplied folder (models.zip) to the “processing” folder inside the QGIS root folder, as follow:
Open QGIS, go to processing > Copy the provided “model” folder> Models icon (red Engine) and choose Open existing model > paste provided “model” folder and replace with existing one.
![add models](https://user-images.githubusercontent.com/8848123/102022925-fa634600-3d9a-11eb-9b5e-51b17d35812f.gif)


![Capture](https://user-images.githubusercontent.com/8848123/102022770-08649700-3d9a-11eb-8b6f-99996676fcc8.PNG)

Required input:
•	Landslide locations with points features 
•	DEM raster
•	Optional: Landslide locations with polygon feature (polygons feature will be converted into points)

## General description of the developed tools in the modeler environment 

## GRID UNIT (GU)

### 2-2-1 “0. GU Extract Landslides area centroid and summary (optional)”

![221](https://user-images.githubusercontent.com/8848123/103148884-91ee6e80-4775-11eb-927b-8376a3255855.jpg)

### 2-2-2 “00. Extract Study area (Main basins)”

![222](https://user-images.githubusercontent.com/8848123/103148898-c2cea380-4775-11eb-954b-a5c301743c2b.jpg)

### 2-2-2 “1.a GU Extract Slope values for original inventory”
![2221](https://user-images.githubusercontent.com/8848123/103148965-5bfdba00-4776-11eb-8dd6-ef20b9ae8cb7.jpg)


### 2-2-3 “1.b GU Extracted Slope values for original inventory statistics”

![223](https://user-images.githubusercontent.com/8848123/103148916-e396f900-4775-11eb-88b9-4aa66cc07b9a.jpg)


### 2-2-4 “2. GU Extract Landslides-free inventory”
![224](https://user-images.githubusercontent.com/8848123/103148923-f6113280-4775-11eb-8e35-dc9421e23d57.jpg)


### 2-2-5 “3.a. GU Extract Training and Testing samples”
![225](https://user-images.githubusercontent.com/8848123/103149126-b0556980-4777-11eb-82f3-969ba14e2dc9.jpg)

### 2-2-6 “3.b. GU Extract conditioning factors values”
![226](https://user-images.githubusercontent.com/8848123/103149139-d1b65580-4777-11eb-90bd-161c9c9a8997.jpg)
-------------------------------------------------------------------------------------------------------------------

## SLOPE UNIT (SU)

### 3-3-1 “0. Extract Study  area (Main basins)”

The tool is like the one mentioned earlier with GU extraction process.
![331](https://user-images.githubusercontent.com/8848123/103149204-7b95e200-4778-11eb-8357-ab305904b077.jpg)
### 3-3-2 “1. SU Landslides extraction”

![332](https://user-images.githubusercontent.com/8848123/103149205-7d5fa580-4778-11eb-9796-2a0a51fbb46f.jpg)

### 3-3-3 “2.a. SU Extract Slope values for original inventory”
![333](https://user-images.githubusercontent.com/8848123/103149209-7f296900-4778-11eb-95b3-adf0a2573143.jpg)

### 3-3-4 “2.b. SU Extracted Slope values for original inventory statistics”
The tools are like the one mentioned earlier with GU extraction process.

### 3-3-5 “3. SU Extract Landslides-free inventory”
![334](https://user-images.githubusercontent.com/8848123/103149341-974db800-4779-11eb-8af7-a930156f6f5a.PNG)


### 3-3-6 “4.a. SU Extract Training and Testing samples”
![335](https://user-images.githubusercontent.com/8848123/103149293-345c2100-4779-11eb-8f04-781932a9be66.PNG)

### 3-3-7 “4.b. SU Extract conditioning factors values”

![226](https://user-images.githubusercontent.com/8848123/103149139-d1b65580-4777-11eb-90bd-161c9c9a8997.jpg)



