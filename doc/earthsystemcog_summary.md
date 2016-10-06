# Earth System CoG summary
A simple guide on how to get climate data netCDF files from www.earthsystemcog.org

## Getting started
1. Go to www.earthsystemcog.org
2. Click create account or follow this link https://esgf.esrl.noaa.gov/user/add/?next=http%253A%252F%252Fwww.earthsystemcog.org%252Fprojects%252Fcog%252F
3. Login and go to the Browse Projects list on the right side of the screen. Each projects contains different reasources, they are not all of intrest to us.
  * For global data go to CMIP5.
  * For regional data go to CORDEX.

## Accesing CMIP5 - global data
1. Press Search for CMIP5 project data or follow this link https://pcmdi.llnl.gov/search/cmip5
2. To the left are different categorial filters that can be played with. Good filters to begin with are:
 * Project-CMIP5
 * Realm-land
 * Variable-tas
3. Press search after choosing filters. 
4. Datasets matching your filters will now come up.
5. To download single netCDF files from the datasets press Show Files and the HTTPServer on the choosen file. 
 * If this is your first time downloading from CMIP5 you have to register.

## Accesing CORDEX - regional data
1. Press Search for CMIP5 project data or follow this link https://esg-dn1.nsc.liu.se/search/cordex/
2. To the left are different categorial filters that can be played with. Good filters to begin with are:
 * Domain-EUR-11
 * Variable-tas
3. Press search after choosing filters. 
4. Datasets matching your filters will now come up.
5. To download single netCDF files from the datasets press Show Files and the HTTPServer on the choosen file. 
 * If this is your first time downloading from CMIP5 you have to register.

## Viewing netCDF files
1. A simple way to view the netCDF files is with ncview it can be downloaded from http://meteora.ucsd.edu/~pierce/ncview_home_page.html
2. Once a nerCDF file is downloaded and opend with ncview the data can be visualized this is done by pressing the variable of intresst.
3. OBS! With most climate data models there is only one variable of interesst often by the same name as the file. Press it and nothing else.

## Variable categori
When choosing a project in earthsystemCoG and searching for data in it there are a lot of different categories to choose from. This text is ment to explain what those different categories are and what the variables in them stand for.

### Project
What project do you want to serch for data in? Often the same as the project you are in but certain projects can have "sub" projects.

### Product
???

### Domain
What region is the data from? The normal regions are:

* AFR - Africa
* ANT - Antartica
* ARC - Arctic
* AUS - Australia
* CAM - Central America
* EAS - East America
* EUR - Europe
* MNA - 
* NAM - 
* SAM - 
* WAS - West America

After the region name there is always a number if the number is high say 44 it means low resolution. If the number is low it means high resolution.

After the number there can be and "i" if it is there it means that the 2D map has been projected on a sphere.

### Institute
Self explanitory. We use smhi

### Driving model
* CNRM-CERFACS-CNRM-CM5 a french model from 1995
* ECMWF-ERAINT is a global atmospheric reanalysis from 1979, continuously updated in real time.
* ICHEC-EC-EARTH Irish model
* IPSL-IPSL-CM5A-MR The Institut Pierre Simon Laplace active since 1995
* MOHC-HadGEM2-ES Met Office Hadley Centre active from 1990 from UK, uses data from the past 100 years to predict the next 100 years
* MPI-M-MPI-ESM-LR Max-Planck-institut for meteorologie German

other things to note
* MR - medium resolution
* LR - low resolution
* A - Atomosphere
* ES - Earth system
* CC - Carbon cycle

### 
