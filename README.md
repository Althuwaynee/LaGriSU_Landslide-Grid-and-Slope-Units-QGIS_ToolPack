# LaGriSU_Landslide-Grid-and-Slope-Units-QGIS_ToolPack

LaGriSU v 0.2 (Landslide Grid and Slope Units): binary (1,0) samples extraction tool pack for landslides mapping in QGIS

**Omar F. AlThuwaynee**, *Developer* 

## Introduction
* LaGriSU, designed specifically for landslide mapping  applications,  developed in QGIS tool box modeler, The  Tool  Pack  does not requires  an  internet  connection or Java runtime environment at any stage (just copy and paste the modules in models library).
* The first version of QGIS.GSU V.01 was released in 2018, presented in online course “” as part of landslide susceptibility mapping tutorials. Since that time, 200 user was download and used the tool, and that let us collect all the complains, bugs, workability issues to be fix in the current V0.2.
* Tool provided a user-friendly experience to systematically learn (open box), visualize and validate the extracted samples stored in many different resultant layers (before and after to be merged), and to update the extracted samples whenever the features homogeneity was disturbed. 
* Furthermore, the tool does not need any programing or advance GIS skills to be executed.

To check the Tool version 0.1, please visit the [Udemy course](https://www.udemy.com/course/susceptibility-auto-mapping-tools-for-trainingtesting-data/)


## Installation

Tool pack modules built of graphical modeler of QGIS [versions](https://qgis.org/downloads/) 3.4.0, 3.6.0 and 3.8.0.

1.	Go to Settings > Options > Processing and under General change to Ignore features with invalid geometries.
2.	Unzip tool pack to the QGIS library

### In order to view the tool pack
we must unzip the supplied folder (models.zip) to the “processing” folder inside the QGIS root folder, as follow:
Open QGIS, go to processing > Copy the provided “model” folder> Models icon (red Engine) and choose Open existing model > paste provided “model” folder and replace with existing one.
![add models](https://user-images.githubusercontent.com/8848123/102022925-fa634600-3d9a-11eb-9b5e-51b17d35812f.gif)


![Capture](https://user-images.githubusercontent.com/8848123/102022770-08649700-3d9a-11eb-8b6f-99996676fcc8.PNG)


## Required input:
•	Landslide locations with points features 
•	DEM raster
•	Optional: Landslide locations with polygon feature (polygons feature will be converted into points)


## 1- GRID UNIT (GU)

### 1-0 “0. GU Extract Landslides area centroid and summary (optional)”

![221](https://user-images.githubusercontent.com/8848123/103148884-91ee6e80-4775-11eb-927b-8376a3255855.jpg)

### 1-1 “00. Extract Study area (Main basins)”

![222](https://user-images.githubusercontent.com/8848123/103148898-c2cea380-4775-11eb-954b-a5c301743c2b.jpg)

### 1-2 “1.a GU Extract Slope values for original inventory”
![2221](https://user-images.githubusercontent.com/8848123/103148965-5bfdba00-4776-11eb-8dd6-ef20b9ae8cb7.jpg)


### 1-3 “1.b GU Extracted Slope values for original inventory statistics”

![223](https://user-images.githubusercontent.com/8848123/103148916-e396f900-4775-11eb-88b9-4aa66cc07b9a.jpg)


### 1-4 “2. GU Extract Landslides-free inventory”
![224](https://user-images.githubusercontent.com/8848123/103148923-f6113280-4775-11eb-8e35-dc9421e23d57.jpg)


### 1-5 “3.a. GU Extract Training and Testing samples”
![225](https://user-images.githubusercontent.com/8848123/103149126-b0556980-4777-11eb-82f3-969ba14e2dc9.jpg)

### 1-6 “3.b. GU Extract conditioning factors values”
![226](https://user-images.githubusercontent.com/8848123/103149139-d1b65580-4777-11eb-90bd-161c9c9a8997.jpg)
-------------------------------------------------------------------------------------------------------------------

## 2-SLOPE UNIT (SU)

### 2-1 “0. Extract Study  area (Main basins)”

The tool is like the one mentioned earlier with GU extraction process.
![331](https://user-images.githubusercontent.com/8848123/103149204-7b95e200-4778-11eb-8357-ab305904b077.jpg)
### 2-2 “1. SU Landslides extraction”

![332](https://user-images.githubusercontent.com/8848123/103149205-7d5fa580-4778-11eb-9796-2a0a51fbb46f.jpg)

### 2-3 “2.a. SU Extract Slope values for original inventory”
![333](https://user-images.githubusercontent.com/8848123/103149209-7f296900-4778-11eb-95b3-adf0a2573143.jpg)

### 2-4 “2.b. SU Extracted Slope values for original inventory statistics”
![2221](https://user-images.githubusercontent.com/8848123/103148965-5bfdba00-4776-11eb-8dd6-ef20b9ae8cb7.jpg)
![223](https://user-images.githubusercontent.com/8848123/103148916-e396f900-4775-11eb-88b9-4aa66cc07b9a.jpg)

### 2-5 “3. SU Extract Landslides-free inventory”
![334](https://user-images.githubusercontent.com/8848123/103149341-974db800-4779-11eb-8af7-a930156f6f5a.PNG)


### 2-6 “4.a. SU Extract Training and Testing samples”
![335](https://user-images.githubusercontent.com/8848123/103149293-345c2100-4779-11eb-8f04-781932a9be66.PNG)

### 2-7 “4.b. SU Extract conditioning factors values”

![226](https://user-images.githubusercontent.com/8848123/103149139-d1b65580-4777-11eb-90bd-161c9c9a8997.jpg)
----------------------------------------------------------------------------------------------------

## GU and SU extraction Tools pack :Case study of landslide inventory 

## 1- GRID UNIT tool pack

![1](https://user-images.githubusercontent.com/8848123/103150558-6627b480-4786-11eb-95ca-623f4e51bd02.png)
![2](https://user-images.githubusercontent.com/8848123/103150559-66c04b00-4786-11eb-9d3f-8c1208c0975d.png)
![3](https://user-images.githubusercontent.com/8848123/103150560-6758e180-4786-11eb-8604-ad6ac3fa4da8.png)
![4](https://user-images.githubusercontent.com/8848123/103150563-6758e180-4786-11eb-8268-96bb408c43e9.png)
![5](https://user-images.githubusercontent.com/8848123/103150564-67f17800-4786-11eb-91a4-cee5bb1d1f4c.png)
![6](https://user-images.githubusercontent.com/8848123/103150565-688a0e80-4786-11eb-89ea-df7fe0b5925d.png)
![7](https://user-images.githubusercontent.com/8848123/103150566-6922a500-4786-11eb-9cc8-04fc29f24320.png)
![8](https://user-images.githubusercontent.com/8848123/103150567-6922a500-4786-11eb-9d53-59c63ddb9d88.png)
![9](https://user-images.githubusercontent.com/8848123/103150568-69bb3b80-4786-11eb-8880-fa108d1b262c.png)
![10](https://user-images.githubusercontent.com/8848123/103150569-69bb3b80-4786-11eb-97e7-81e34d31a7ee.png)
![11](https://user-images.githubusercontent.com/8848123/103150570-6a53d200-4786-11eb-82db-8f055e27f2b5.png)
![12](https://user-images.githubusercontent.com/8848123/103150571-6aec6880-4786-11eb-85e8-21f6d3e99955.png)
![13](https://user-images.githubusercontent.com/8848123/103150572-6aec6880-4786-11eb-945b-63819912bf8b.png)
![14](https://user-images.githubusercontent.com/8848123/103150552-62942d80-4786-11eb-97ee-ffc4fe45115e.png)
![15](https://user-images.githubusercontent.com/8848123/103150553-63c55a80-4786-11eb-8087-06f819b70580.png)
![16](https://user-images.githubusercontent.com/8848123/103150554-645df100-4786-11eb-87fe-f007b609b1d0.png)
![17](https://user-images.githubusercontent.com/8848123/103150556-658f1e00-4786-11eb-9ed9-0e37da6fd878.png)
![18](https://user-images.githubusercontent.com/8848123/103150591-a38c4200-4786-11eb-800b-db14f88db5dc.png)


## 2- SLOPE UNIT tool pack

We will start over the process with extraction of study area and data entry of landslide locations and DEM raster only. 

![19](https://user-images.githubusercontent.com/8848123/103150645-3cbb5880-4787-11eb-9ab1-ef428a4c414f.png)
![20](https://user-images.githubusercontent.com/8848123/103150646-3cbb5880-4787-11eb-8cc2-ebd04984f200.png)
![21](https://user-images.githubusercontent.com/8848123/103150647-3d53ef00-4787-11eb-8503-9e3e5ad04156.png)
![22](https://user-images.githubusercontent.com/8848123/103150649-3f1db280-4787-11eb-8815-3ea8ca454be7.png)
![23](https://user-images.githubusercontent.com/8848123/103150650-404edf80-4787-11eb-88fa-c23be160a5c4.png)
![24](https://user-images.githubusercontent.com/8848123/103150651-40e77600-4787-11eb-83af-bf4087718260.png)
![25](https://user-images.githubusercontent.com/8848123/103150652-40e77600-4787-11eb-8733-930bb29e33c1.png)
![26](https://user-images.githubusercontent.com/8848123/103150653-41800c80-4787-11eb-9915-7e5fd5ba012c.png)
![27](https://user-images.githubusercontent.com/8848123/103150654-4218a300-4787-11eb-9516-3090d9c019dc.png)
![28](https://user-images.githubusercontent.com/8848123/103150657-4349d000-4787-11eb-9b99-a2dfc62819b9.png)
![29](https://user-images.githubusercontent.com/8848123/103150660-43e26680-4787-11eb-93d8-7606150655b9.png)
![30](https://user-images.githubusercontent.com/8848123/103150662-447afd00-4787-11eb-96e3-545ae7d6f760.png)
![31](https://user-images.githubusercontent.com/8848123/103150663-45139380-4787-11eb-933a-d6096e805bfb.png)
![32](https://user-images.githubusercontent.com/8848123/103150664-45ac2a00-4787-11eb-8bbc-da439c8cde66.png)
![33](https://user-images.githubusercontent.com/8848123/103150644-3b8a2b80-4787-11eb-8d8a-1e6d6706c753.png)

![results](https://user-images.githubusercontent.com/8848123/103150665-45ac2a00-4787-11eb-908a-04b6d14b8025.jpg)

